from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.controllers.prediction_controller import PredictionController
from app.middleware.auth_middleware import get_current_user_id


router = APIRouter(prefix="/api/predictions", tags=["Predictions"])
controller = PredictionController()


@router.post("/predict", status_code=status.HTTP_201_CREATED, summary="Upload a plant image and predict disease")
async def predict(file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)):
    return await controller.predict(user_id, file)


@router.get("/history", summary="Get authenticated user's prediction history")
async def history(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    user_id: str = Depends(get_current_user_id),
):
    return await controller.history(user_id, limit, skip)


@router.get("/{prediction_id}", summary="Get a prediction by id")
async def get_prediction(prediction_id: str, user_id: str = Depends(get_current_user_id)):
    return await controller.get_prediction(prediction_id, user_id)


@router.delete("/{prediction_id}", summary="Delete a prediction by id")
async def delete_prediction(prediction_id: str, user_id: str = Depends(get_current_user_id)):
    return await controller.delete_prediction(prediction_id, user_id)
