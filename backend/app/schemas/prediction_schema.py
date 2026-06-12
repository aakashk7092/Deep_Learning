from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ModelPrediction(BaseModel):
    plant_name: str
    disease_name: str
    confidence: float = Field(..., ge=0, le=1)
    severity: str


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    image_path: str
    processed_image_path: Optional[str] = None
    plant_name: str
    disease_name: str
    confidence: float = Field(..., ge=0, le=1)
    severity: str
    symptoms: List[str] = Field(default_factory=list)
    causes: List[str] = Field(default_factory=list)
    prevention: List[str] = Field(default_factory=list)
    treatment: List[str] = Field(default_factory=list)
    recommended_fertilizers: List[str] = Field(default_factory=list)
    recommended_fungicides: List[str] = Field(default_factory=list)
    created_at: datetime


class PredictionListResponse(BaseModel):
    total: int
    items: List[PredictionResponse]


class DashboardStatsResponse(BaseModel):
    total_predictions: int
    healthy_plants: int
    diseased_plants: int
    average_confidence: float
    most_common_disease: Optional[str] = None
    recent_predictions: List[PredictionResponse]
