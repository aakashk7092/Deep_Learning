from typing import List

from pydantic import BaseModel, ConfigDict, Field


class DiseaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    plant_name: str
    disease_name: str
    description: str = ""
    symptoms: List[str] = Field(default_factory=list)
    causes: List[str] = Field(default_factory=list)
    prevention: List[str] = Field(default_factory=list)
    treatment: List[str] = Field(default_factory=list)
    recommended_fertilizers: List[str] = Field(default_factory=list)
    recommended_fungicides: List[str] = Field(default_factory=list)
