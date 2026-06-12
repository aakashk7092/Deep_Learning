import logging
from pathlib import Path
from typing import Any, Dict

from bson import ObjectId
from fastapi import UploadFile

from app.config.database import predictions_collection
from app.config.settings import get_settings
from app.middleware.upload_middleware import UploadValidator
from app.models.Prediction import PredictionModel
from app.services.disease_service import DiseaseService
from app.utils.image_processor import ImageProcessor
from app.utils.response_handler import forbidden, not_found


logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self) -> None:
        self.disease_service = DiseaseService()

    async def predict(self, user_id: str, file: UploadFile) -> Dict[str, Any]:
        content = await UploadValidator.validate_image(file)
        settings = get_settings()
        filename = UploadValidator.secure_filename(file.filename or "plant.jpg")
        original_path = settings.original_upload_dir / filename
        processed_path = settings.processed_upload_dir / f"{Path(filename).stem}.jpg"

        original_path.write_bytes(content)
        image_array = ImageProcessor.preprocess_image(original_path, processed_path)
        model_prediction = ImageProcessor.predict(image_array)
        disease_details = await self.disease_service.get_details(model_prediction.plant_name, model_prediction.disease_name)

        document = PredictionModel.create_document(
            user_id=user_id,
            image_path=str(original_path.relative_to(settings.upload_dir.parent)),
            processed_image_path=str(processed_path.relative_to(settings.upload_dir.parent)),
            plant_name=model_prediction.plant_name,
            disease_name=model_prediction.disease_name,
            confidence=model_prediction.confidence,
            severity=model_prediction.severity,
            symptoms=disease_details.get("symptoms", []),
            causes=disease_details.get("causes", []),
            prevention=disease_details.get("prevention", []),
            treatment=disease_details.get("treatment", []),
            recommended_fertilizers=disease_details.get("recommended_fertilizers", []),
            recommended_fungicides=disease_details.get("recommended_fungicides", []),
        )
        result = await predictions_collection().insert_one(document)
        created = await predictions_collection().find_one({"_id": result.inserted_id})
        return PredictionModel.public_document(created)

    async def history(self, user_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        query = {"user_id": user_id}
        total = await predictions_collection().count_documents(query)
        cursor = predictions_collection().find(query).sort("created_at", -1).skip(skip).limit(limit)
        items = [PredictionModel.public_document(document) async for document in cursor]
        return {"total": total, "items": items}

    async def get_prediction(self, prediction_id: str, user_id: str) -> Dict[str, Any]:
        document = await self._get_owned_prediction(prediction_id, user_id)
        return PredictionModel.public_document(document)

    async def delete_prediction(self, prediction_id: str, user_id: str) -> None:
        document = await self._get_owned_prediction(prediction_id, user_id)
        await predictions_collection().delete_one({"_id": document["_id"]})

    async def _get_owned_prediction(self, prediction_id: str, user_id: str) -> Dict[str, Any]:
        if not ObjectId.is_valid(prediction_id):
            not_found("Prediction not found")
        document = await predictions_collection().find_one({"_id": ObjectId(prediction_id)})
        if not document:
            not_found("Prediction not found")
        if document["user_id"] != user_id:
            forbidden("You do not have access to this prediction")
        return document
