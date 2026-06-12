from typing import Any, Dict

from app.config.database import predictions_collection
from app.models.Prediction import PredictionModel


class DashboardService:
    async def stats(self, user_id: str) -> Dict[str, Any]:
        query = {"user_id": user_id}
        total = await predictions_collection().count_documents(query)
        healthy = await predictions_collection().count_documents({**query, "disease_name": {"$regex": "^healthy$", "$options": "i"}})
        diseased = total - healthy

        confidence_pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "average": {"$avg": "$confidence"}}},
        ]
        confidence_rows = await predictions_collection().aggregate(confidence_pipeline).to_list(length=1)
        average_confidence = round(float(confidence_rows[0]["average"]), 4) if confidence_rows else 0.0

        common_pipeline = [
            {"$match": {**query, "disease_name": {"$not": {"$regex": "^healthy$", "$options": "i"}}}},
            {"$group": {"_id": "$disease_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1},
        ]
        common_rows = await predictions_collection().aggregate(common_pipeline).to_list(length=1)
        most_common_disease = common_rows[0]["_id"] if common_rows else None

        recent_cursor = predictions_collection().find(query).sort("created_at", -1).limit(5)
        recent_predictions = [PredictionModel.public_document(document) async for document in recent_cursor]
        return {
            "total_predictions": total,
            "healthy_plants": healthy,
            "diseased_plants": diseased,
            "average_confidence": average_confidence,
            "most_common_disease": most_common_disease,
            "recent_predictions": recent_predictions,
        }
