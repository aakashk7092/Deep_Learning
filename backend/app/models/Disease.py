from typing import Any, Dict, List


class DiseaseModel:
    collection_name = "diseases"

    @staticmethod
    def public_document(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "plant_name": document["plant_name"],
            "disease_name": document["disease_name"],
            "description": document.get("description", ""),
            "symptoms": document.get("symptoms", []),
            "causes": document.get("causes", []),
            "prevention": document.get("prevention", []),
            "treatment": document.get("treatment", []),
            "recommended_fertilizers": document.get("recommended_fertilizers", []),
            "recommended_fungicides": document.get("recommended_fungicides", []),
        }

    @staticmethod
    def fallback_details(plant_name: str, disease_name: str) -> Dict[str, List[str] | str]:
        is_healthy = disease_name.lower() == "healthy"
        return {
            "plant_name": plant_name,
            "disease_name": disease_name,
            "description": "No disease indicators were detected." if is_healthy else f"{disease_name} detected on {plant_name}.",
            "symptoms": [] if is_healthy else ["Visible discoloration, spots, wilting, or lesions may be present."],
            "causes": [] if is_healthy else ["Disease pressure can be influenced by humidity, infected debris, poor airflow, pests, or nutrient stress."],
            "prevention": ["Maintain good sanitation, proper watering, adequate spacing, and regular plant monitoring."],
            "treatment": ["Continue routine care and monitoring."] if is_healthy else ["Remove affected plant material, isolate severely infected plants, and apply locally approved treatment if symptoms progress."],
            "recommended_fertilizers": ["Balanced NPK fertilizer based on soil test results."],
            "recommended_fungicides": [] if is_healthy else ["Use a crop-appropriate fungicide approved for your location and follow label directions."],
        }
