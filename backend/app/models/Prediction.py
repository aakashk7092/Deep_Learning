from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId


class PredictionModel:
    collection_name = "predictions"

    @staticmethod
    def create_document(
        user_id: str,
        image_path: str,
        plant_name: str,
        disease_name: str,
        confidence: float,
        severity: str,
        symptoms: List[str],
        causes: List[str],
        prevention: List[str],
        treatment: List[str],
        recommended_fertilizers: List[str],
        recommended_fungicides: List[str],
        processed_image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "image_path": image_path,
            "processed_image_path": processed_image_path,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "confidence": confidence,
            "severity": severity,
            "symptoms": symptoms,
            "causes": causes,
            "prevention": prevention,
            "treatment": treatment,
            "recommended_fertilizers": recommended_fertilizers,
            "recommended_fungicides": recommended_fungicides,
            "created_at": datetime.now(timezone.utc),
        }

    @staticmethod
    def public_document(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "user_id": document["user_id"],
            "image_path": document["image_path"],
            "processed_image_path": document.get("processed_image_path"),
            "plant_name": document["plant_name"],
            "disease_name": document["disease_name"],
            "confidence": document["confidence"],
            "severity": document["severity"],
            "symptoms": document.get("symptoms", []),
            "causes": document.get("causes", []),
            "prevention": document.get("prevention", []),
            "treatment": document.get("treatment", []),
            "recommended_fertilizers": document.get("recommended_fertilizers", []),
            "recommended_fungicides": document.get("recommended_fungicides", []),
            "created_at": document["created_at"],
        }

    @staticmethod
    def object_id(value: str) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid prediction id")
        return ObjectId(value)
