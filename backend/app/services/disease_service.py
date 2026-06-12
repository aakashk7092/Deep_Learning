from typing import Any, Dict

from app.config.database import diseases_collection
from app.models.Disease import DiseaseModel


class DiseaseService:
    async def get_details(self, plant_name: str, disease_name: str) -> Dict[str, Any]:
        document = await diseases_collection().find_one(
            {
                "plant_name": {"$regex": f"^{plant_name}$", "$options": "i"},
                "disease_name": {"$regex": f"^{disease_name}$", "$options": "i"},
            }
        )
        if document:
            return DiseaseModel.public_document(document)
        return DiseaseModel.fallback_details(plant_name, disease_name)
