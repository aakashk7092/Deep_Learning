# Plant Disease Detection System Technical Report

## 1. System Overview

The Plant Disease Detection System is a full-stack AI application that allows authenticated users to upload plant leaf images, receive disease predictions, review treatment guidance, and track prediction history over time.

The system is organized into three main application layers:

- Frontend: React, Vite, and TailwindCSS user interface.
- Backend: FastAPI application with JWT authentication, MongoDB persistence, file upload handling, and prediction orchestration.
- ML service: TensorFlow/Keras training and inference pipeline using EfficientNetB0 as the primary production model.

The main runtime workflow is:

1. A user registers or logs in from the React frontend.
2. The backend returns a JWT access token and refresh token.
3. The frontend stores the access token and sends it as a Bearer token on protected API calls.
4. The user uploads a plant leaf image from the Prediction page.
5. The backend validates the image, stores the original file, preprocesses it, loads the trained TensorFlow model, and runs inference.
6. The backend enriches the ML result with disease details from MongoDB.
7. The prediction is stored in the `predictions` collection.
8. The frontend displays the plant name, disease name, confidence, severity, symptoms, causes, prevention, treatment, fertilizers, and fungicides.
9. History and dashboard pages read stored prediction records from MongoDB through protected backend APIs.

## 2. Text-Based Architecture Diagram

```text
+-----------------------------+
| React + Vite Frontend       |
|                             |
| Pages:                      |
| - Home                      |
| - Register/Login            |
| - Prediction                |
| - Dashboard                 |
| - History                   |
| - Profile                   |
|                             |
| Services: Axios API client  |
+-------------+---------------+
              |
              | HTTPS / JSON / multipart-form-data
              | Authorization: Bearer <access_token>
              v
+-------------+---------------+
| FastAPI Backend             |
|                             |
| Routes:                     |
| - /api/auth/*               |
| - /api/predictions/*        |
| - /api/dashboard/stats      |
|                             |
| Services:                   |
| - AuthService               |
| - PredictionService         |
| - DiseaseService            |
| - DashboardService          |
+------+--------------+-------+
       |              |
       |              |
       v              v
+------+-------+   +--+-----------------------------+
| MongoDB      |   | Local File Storage             |
|              |   |                                |
| collections: |   | backend/uploads/original       |
| - users      |   | backend/uploads/processed      |
| - diseases   |   | backend/uploads/predictions    |
| - predictions|   |                                |
+--------------+   +--------------------------------+
       ^
       |
       | disease metadata and prediction records
       |
+------+-------------------------------------------+
| ML Service                                        |
|                                                   |
| Training:                                         |
| - PlantVillage dataset split                      |
| - preprocessing and augmentation                  |
| - EfficientNetB0 transfer learning                |
| - evaluation reports                              |
|                                                   |
| Runtime artifacts:                                |
| - saved_models/best_model.keras                   |
| - saved_models/labels.json                        |
| - reports/*                                       |
+---------------------------------------------------+
```

## 3. End-to-End Prediction Data Flow

```text
User
  |
  | selects image in UploadBox
  v
Frontend Prediction Page
  |
  | FormData field: file
  | POST /api/predictions/predict
  | Authorization: Bearer JWT
  v
FastAPI Prediction Route
  |
  | validates token with auth middleware
  v
PredictionController
  |
  v
PredictionService
  |
  | validate MIME type and image integrity
  | save original image
  | resize to 224 x 224
  | normalize pixels to 0-1
  | save processed image
  v
ImageProcessor
  |
  | load saved_models/best_model.keras
  | load saved_models/labels.json
  | run TensorFlow prediction
  v
DiseaseService
  |
  | fetch disease metadata from MongoDB diseases collection
  | fallback to generic guidance if metadata is absent
  v
MongoDB predictions collection
  |
  | insert prediction history record
  v
Backend JSON Response
  |
  v
Frontend PredictionCard, DiseaseInfoCard, TreatmentCard
```

## 4. Major Components and Responsibilities

| Layer | Component | Responsibility |
|---|---|---|
| Frontend | `App.jsx` | Hosts the main React application and route tree. |
| Frontend | `MainLayout.jsx` | Provides shared layout structure, navigation, and footer. |
| Frontend | `Navbar.jsx` | Displays primary navigation links and auth-aware navigation. |
| Frontend | `ProtectedRoute.jsx` | Restricts pages that require authentication. |
| Frontend | `AuthContext.jsx` | Stores user session state, persists token and user details in local storage, and exposes login/register/logout actions. |
| Frontend | `PredictionContext.jsx` | Stores current prediction state and prediction loading/progress state. |
| Frontend | `api.js` | Axios client with base URL, timeout, JWT request interceptor, and response error normalization. |
| Frontend | `authService.js` | Calls backend authentication and profile APIs. |
| Frontend | `predictionService.js` | Uploads images, fetches history, and deletes prediction records. |
| Frontend | `dashboardService.js` | Fetches dashboard aggregate statistics. |
| Backend | `main.py` | Creates the FastAPI app, configures CORS, mounts uploads, registers routers, and defines global exception handlers. |
| Backend | `settings.py` | Reads environment variables and centralizes paths, JWT settings, CORS origins, upload limits, and model paths. |
| Backend | `database.py` | Opens and closes Motor MongoDB connections and creates indexes. |
| Backend | `auth_routes.py` | Exposes registration, login, refresh, current user, profile update, and password change endpoints. |
| Backend | `prediction_routes.py` | Exposes image prediction, history, single prediction, and delete endpoints. |
| Backend | `dashboard_routes.py` | Exposes dashboard statistics endpoint. |
| Backend | `AuthService` | Hashes passwords, verifies credentials, issues JWTs, refreshes tokens, and updates user data. |
| Backend | `PredictionService` | Coordinates upload validation, file storage, preprocessing, ML inference, disease lookup, and MongoDB persistence. |
| Backend | `DiseaseService` | Reads disease metadata and treatment guidance from MongoDB. |
| Backend | `DashboardService` | Aggregates prediction counts, healthy/diseased counts, average confidence, most common disease, and recent predictions. |
| Backend | `ImageProcessor` | Converts images to model-ready tensors and runs TensorFlow inference. |
| Backend | `UploadValidator` | Validates MIME type, file size, and real image content. |
| ML Service | `split_dataset.py` | Splits PlantVillage raw images into train, validation, and test folders. |
| ML Service | `augmentations.py` | Defines reusable random flip, rotation, zoom, contrast, brightness, and translation pipeline. |
| ML Service | `efficientnetb0.py` | Builds the production transfer-learning model. |
| ML Service | `train.py` | Trains a selected model, writes labels, exports artifacts, and generates reports. |
| ML Service | `evaluate.py` | Computes metrics and writes evaluation artifacts. |
| ML Service | `gradcam.py` | Generates Grad-CAM heatmaps and overlay images. |
| ML Service | `predictor.py` | Provides production inference with top predictions and optional Grad-CAM output. |
| Database | `users` | Stores user profile, password hash, role, timestamps, and last login. |
| Database | `predictions` | Stores prediction results and disease guidance for each user upload. |
| Database | `diseases` | Stores disease descriptions, symptoms, causes, prevention, treatment, fertilizers, and fungicides. |
| File Storage | `uploads/original` | Stores the user-uploaded source image. |
| File Storage | `uploads/processed` | Stores resized and normalized visual copy used for prediction. |
| File Storage | `uploads/predictions` | Reserved for prediction artifacts such as explainability overlays or derived outputs. |

## 5. Frontend Architecture

The frontend is a React application created with Vite. TailwindCSS provides styling utilities, while Axios handles HTTP requests to the FastAPI backend.

### Pages

- `Home`: Landing and entry point for the application.
- `Register`: Collects full name, email, and password, then calls `POST /api/auth/register`.
- `Login`: Authenticates an existing user through `POST /api/auth/login`.
- `Prediction`: Lets users upload a plant image and displays the prediction result.
- `Dashboard`: Displays aggregate statistics such as total predictions, healthy plants, diseased plants, average confidence, and recent predictions.
- `History`: Displays past predictions and allows deletion.
- `Profile`: Displays and updates authenticated user profile information.
- `About`: Provides project information.

### Components

- `UploadBox`: Receives an image file and calls the prediction workflow.
- `PredictionCard`: Displays the main prediction result: plant, disease, confidence, and severity.
- `DiseaseInfoCard`: Displays symptoms, causes, and prevention information.
- `TreatmentCard`: Displays treatment, fertilizers, and fungicides.
- `HistoryTable`: Displays past predictions.
- `DashboardCard`: Displays dashboard counters and metrics.
- `Loader`: Shows loading state during prediction.
- `ProtectedRoute`: Blocks unauthenticated access to protected pages.

### API Consumption

The frontend uses `frontend/src/services/api.js` as the shared Axios client. It:

- Reads the JWT from local storage.
- Adds `Authorization: Bearer <token>` to outgoing protected requests.
- Uses `VITE_API_BASE_URL` or `http://localhost:8000` as the backend base URL.
- Normalizes API errors into JavaScript `Error` objects.

## 6. Backend Architecture

The backend uses FastAPI with clean separation between routes, controllers, services, schemas, models, middleware, and utilities.

```text
backend/app
  config/
    settings.py       Environment variables and paths
    database.py       MongoDB connection and indexes
  routes/
    auth_routes.py
    prediction_routes.py
    dashboard_routes.py
  controllers/
    auth_controller.py
    prediction_controller.py
    dashboard_controller.py
  services/
    auth_service.py
    prediction_service.py
    disease_service.py
    dashboard_service.py
  middleware/
    auth_middleware.py
    upload_middleware.py
  models/
    User.py
    Prediction.py
    Disease.py
  schemas/
    user_schema.py
    prediction_schema.py
    disease_schema.py
  utils/
    jwt_handler.py
    image_processor.py
    response_handler.py
  main.py
```

### Request Routing Pattern

The backend follows this request flow:

```text
FastAPI route
  -> Controller
  -> Service
  -> Utility or Database Collection
  -> Pydantic response-ready data
  -> JSON response
```

Routes handle HTTP-specific details. Controllers keep endpoints thin and delegate business behavior. Services contain core application logic. Utilities handle shared concerns such as JWTs, image preprocessing, response formatting, and upload validation.

## 7. Authentication and Protected Routes

Authentication is based on JWT access tokens and refresh tokens.

### Registration

1. User submits full name, email, and password.
2. Backend validates the request with Pydantic.
3. Password is hashed with Passlib bcrypt.
4. User record is inserted into MongoDB.
5. Backend returns user data, access token, and refresh token.

### Login

1. User submits email and password.
2. Backend finds the user by email.
3. Password is verified against `password_hash`.
4. `last_login` is updated.
5. Backend returns new tokens.

### Protected APIs

Protected backend routes depend on `get_current_user_id`. The middleware:

1. Reads `Authorization: Bearer <token>`.
2. Decodes and validates the JWT.
3. Ensures token type is `access`.
4. Loads the user from MongoDB.
5. Passes the authenticated user id to the route.

Protected routes include:

- `GET /api/auth/me`
- `PUT /api/auth/profile`
- `PUT /api/auth/change-password`
- `POST /api/predictions/predict`
- `GET /api/predictions/history`
- `GET /api/predictions/{prediction_id}`
- `DELETE /api/predictions/{prediction_id}`
- `GET /api/dashboard/stats`

## 8. Database Design

MongoDB is accessed asynchronously through Motor. The backend creates indexes for email uniqueness, prediction history sorting, and disease lookup.

### `users`

```json
{
  "_id": "ObjectId",
  "full_name": "Aakash Kumar",
  "email": "aakash@example.com",
  "password_hash": "$2b$...",
  "avatar": null,
  "role": "user",
  "created_at": "2026-06-12T10:00:00Z",
  "updated_at": "2026-06-12T10:00:00Z",
  "last_login": "2026-06-12T10:30:00Z"
}
```

### `predictions`

```json
{
  "_id": "ObjectId",
  "user_id": "user-object-id",
  "image_path": "uploads/original/leaf.jpg",
  "processed_image_path": "uploads/processed/leaf.jpg",
  "plant_name": "Tomato",
  "disease_name": "Late Blight",
  "confidence": 0.98,
  "severity": "Severe",
  "symptoms": ["Dark lesions", "Water-soaked spots"],
  "causes": ["High humidity", "Infected plant debris"],
  "prevention": ["Improve airflow", "Avoid overhead watering"],
  "treatment": ["Remove infected foliage", "Apply approved fungicide"],
  "recommended_fertilizers": ["Balanced NPK fertilizer"],
  "recommended_fungicides": ["Copper-based fungicide"],
  "created_at": "2026-06-12T10:45:00Z"
}
```

### `diseases`

```json
{
  "_id": "ObjectId",
  "plant_name": "Tomato",
  "disease_name": "Late Blight",
  "description": "A destructive disease caused by Phytophthora infestans.",
  "symptoms": ["Dark leaf lesions", "White mold under humid conditions"],
  "causes": ["Cool wet weather", "Infected seed or debris"],
  "prevention": ["Use resistant varieties", "Avoid wet foliage"],
  "treatment": ["Remove infected parts", "Use approved fungicide"],
  "recommended_fertilizers": ["Balanced NPK"],
  "recommended_fungicides": ["Mancozeb", "Copper oxychloride"]
}
```

## 9. File Upload and Storage Workflow

The backend stores uploaded and derived images under `backend/uploads`.

```text
backend/uploads/
  original/
    <uuid>.jpg        Original validated user upload
  processed/
    <uuid>.jpg        224 x 224 RGB processed copy
  predictions/
    <uuid>_gradcam.jpg or other derived artifacts
```

Prediction upload flow:

1. Frontend sends multipart form data with field name `file`.
2. Backend validates content type: JPEG, PNG, or WEBP.
3. Backend checks file size against `MAX_UPLOAD_SIZE_MB`.
4. Pillow verifies the file is a valid image.
5. Backend writes the original file into `uploads/original`.
6. The image is converted to RGB, resized to 224 x 224, normalized to 0-1, and stored as a processed copy.
7. The processed tensor is passed to the TensorFlow model.
8. Prediction metadata is saved in MongoDB with file paths.

## 10. ML Service Workflow

The ML service is responsible for dataset preparation, model training, evaluation, explainability, and production inference artifacts.

```text
PlantVillage raw dataset
  |
  v
preprocessing/split_dataset.py
  |
  | 70 percent train
  | 15 percent validation
  | 15 percent test
  v
datasets/processed/train, val, test
  |
  v
preprocessing/data_loader.py
  |
  | resize 224 x 224
  | RGB
  | normalize 0-1
  v
models/efficientnetb0.py
  |
  | data augmentation
  | EfficientNetB0 backbone
  | global average pooling
  | batch normalization
  | dropout
  | dense classification head
  v
training/train.py
  |
  | early stopping
  | reduce LR on plateau
  | model checkpoint
  | TensorBoard logging
  v
saved_models/best_model.keras
saved_models/best_model.h5
saved_models/labels.json
saved_models/history.json
saved_models/model_metadata.json
reports/*
```

### Preprocessing

Images are loaded as RGB, resized to 224 x 224, converted to NumPy or TensorFlow tensors, and normalized to the range 0-1. This ensures that training and inference use the same input shape and value range.

### Data Augmentation

The augmentation pipeline includes:

- Random flip
- Random rotation
- Random zoom
- Random contrast
- Random brightness
- Random translation

Augmentation is applied during training to improve generalization and reduce overfitting.

### Supported Models

The ML service includes four model builders:

- Custom CNN
- MobileNetV2
- ResNet50
- EfficientNetB0

EfficientNetB0 is the primary production model because it provides a strong balance between accuracy, parameter efficiency, and transfer-learning performance.

### EfficientNetB0 Architecture

```text
Image Input: 224 x 224 x 3
  |
Data Augmentation
  |
EfficientNetB0 ImageNet Backbone
  |
GlobalAveragePooling2D
  |
BatchNormalization
  |
Dropout(0.3)
  |
Dense(512, relu)
  |
Dropout(0.3)
  |
Dense(num_classes, softmax)
```

### Training

Training uses:

- Loss: categorical crossentropy
- Optimizer: Adam
- Initial learning rate: 0.001
- Epochs: 50
- Batch size: 32
- Metrics: accuracy, precision, recall, AUC
- Callbacks: early stopping, reduce learning rate on plateau, model checkpointing, TensorBoard

### Evaluation

Evaluation generates:

- Accuracy
- Precision
- Recall
- F1 score
- Confusion matrix
- Classification report
- ROC curves
- Prediction examples

Reports are written to `ml-service/reports`.

### Grad-CAM Explainability

Grad-CAM highlights image regions that contributed most strongly to the predicted class. The pipeline:

1. Finds the last convolutional layer.
2. Computes gradients of the predicted class score with respect to the feature maps.
3. Builds a heatmap from weighted activations.
4. Resizes the heatmap to 224 x 224.
5. Overlays the heatmap on the original image.
6. Saves the explainability image.

The inference output can include:

```json
{
  "plant_name": "Tomato",
  "disease_name": "Late Blight",
  "confidence": 0.98,
  "severity": "Severe",
  "top_predictions": [
    { "label": "Tomato__Late_blight", "confidence": 0.98 },
    { "label": "Tomato__Early_blight", "confidence": 0.01 }
  ],
  "gradcam_image": "ml-service/reports/gradcam/sample_gradcam.jpg"
}
```

## 11. API Examples

### Register

Request:

```http
POST /api/auth/register
Content-Type: application/json
```

```json
{
  "full_name": "Aakash Kumar",
  "email": "aakash@example.com",
  "password": "StrongPass123"
}
```

Response:

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "665f1f9e5d6f2d5a1f123456",
      "full_name": "Aakash Kumar",
      "email": "aakash@example.com",
      "avatar": null,
      "role": "user",
      "created_at": "2026-06-12T10:00:00Z",
      "updated_at": "2026-06-12T10:00:00Z",
      "last_login": null
    },
    "access_token": "jwt-access-token",
    "refresh_token": "jwt-refresh-token",
    "token_type": "bearer"
  }
}
```

### Login

Request:

```http
POST /api/auth/login
Content-Type: application/json
```

```json
{
  "email": "aakash@example.com",
  "password": "StrongPass123"
}
```

Response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "665f1f9e5d6f2d5a1f123456",
      "full_name": "Aakash Kumar",
      "email": "aakash@example.com",
      "avatar": null,
      "role": "user",
      "created_at": "2026-06-12T10:00:00Z",
      "updated_at": "2026-06-12T10:30:00Z",
      "last_login": "2026-06-12T10:30:00Z"
    },
    "access_token": "jwt-access-token",
    "refresh_token": "jwt-refresh-token",
    "token_type": "bearer"
  }
}
```

### Predict Disease

Request:

```http
POST /api/predictions/predict
Authorization: Bearer jwt-access-token
Content-Type: multipart/form-data
```

Form data:

```text
file: leaf-image.jpg
```

Response:

```json
{
  "success": true,
  "message": "Prediction completed successfully",
  "data": {
    "id": "666012345d6f2d5a1f123456",
    "user_id": "665f1f9e5d6f2d5a1f123456",
    "image_path": "uploads/original/4f8a9c.jpg",
    "processed_image_path": "uploads/processed/4f8a9c.jpg",
    "plant_name": "Tomato",
    "disease_name": "Late Blight",
    "confidence": 0.98,
    "severity": "Severe",
    "symptoms": ["Dark lesions", "Water-soaked spots"],
    "causes": ["Cool wet weather", "Infected debris"],
    "prevention": ["Improve airflow", "Avoid overhead watering"],
    "treatment": ["Remove infected leaves", "Apply approved fungicide"],
    "recommended_fertilizers": ["Balanced NPK fertilizer"],
    "recommended_fungicides": ["Copper oxychloride"],
    "created_at": "2026-06-12T10:45:00Z"
  }
}
```

### Prediction History

Request:

```http
GET /api/predictions/history?limit=20&skip=0
Authorization: Bearer jwt-access-token
```

Response:

```json
{
  "success": true,
  "message": "Prediction history fetched successfully",
  "data": {
    "total": 2,
    "items": [
      {
        "id": "666012345d6f2d5a1f123456",
        "user_id": "665f1f9e5d6f2d5a1f123456",
        "image_path": "uploads/original/4f8a9c.jpg",
        "processed_image_path": "uploads/processed/4f8a9c.jpg",
        "plant_name": "Tomato",
        "disease_name": "Late Blight",
        "confidence": 0.98,
        "severity": "Severe",
        "symptoms": [],
        "causes": [],
        "prevention": [],
        "treatment": [],
        "recommended_fertilizers": [],
        "recommended_fungicides": [],
        "created_at": "2026-06-12T10:45:00Z"
      }
    ]
  }
}
```

### Dashboard Stats

Request:

```http
GET /api/dashboard/stats
Authorization: Bearer jwt-access-token
```

Response:

```json
{
  "success": true,
  "message": "Dashboard stats fetched successfully",
  "data": {
    "total_predictions": 42,
    "healthy_plants": 12,
    "diseased_plants": 30,
    "average_confidence": 0.9342,
    "most_common_disease": "Early Blight",
    "recent_predictions": []
  }
}
```

## 12. Dashboard Statistics

Dashboard statistics are generated by querying the authenticated user's prediction records.

The backend calculates:

- Total predictions: count of all records for the user.
- Healthy plants: records where `disease_name` is `Healthy`.
- Diseased plants: total minus healthy.
- Average confidence: average of `confidence` across user predictions.
- Most common disease: most frequent non-healthy disease.
- Recent predictions: five newest prediction records sorted by `created_at`.

The frontend consumes `GET /api/dashboard/stats` and maps backend snake_case fields to UI-friendly camelCase fields.

## 13. Folder Structure Explanation

```text
plant desease Detection/
  frontend/
    src/
      pages/              Page-level React screens
      components/         Reusable UI components
      services/           Axios API clients
      context/            React context providers
      hooks/              Custom hooks for auth and prediction state
      utils/              Constants, validators, formatting helpers
      layouts/            Shared page layout

  backend/
    app/
      config/             Settings and database connection
      controllers/        Request orchestration layer
      middleware/         Auth and upload validation helpers
      models/             MongoDB document mapping helpers
      routes/             FastAPI routers
      schemas/            Pydantic request and response schemas
      services/           Business logic
      utils/              JWT, image, and response utilities
      main.py             FastAPI application entry point
    uploads/
      original/           Original uploaded images
      processed/          Resized processed images
      predictions/        Prediction artifacts

  ml-service/
    datasets/
      raw/                PlantVillage class folders before splitting
      processed/          Generated train, val, and test splits
      sample_images/      Local sample images for testing
    preprocessing/        Loading, preprocessing, augmentation, splitting
    models/               CNN, MobileNetV2, ResNet50, EfficientNetB0
    training/             Training, evaluation, metrics, Grad-CAM
    inference/            Production prediction pipeline
    saved_models/         Trained model and labels
    reports/              Metrics, plots, reports, artifact status
    utils/                Shared config, logging, helpers

  docs/
    TECHNICAL_REPORT.md   This report
```

## 14. Environment Variables

The backend uses environment variables from `backend/.env`.

```text
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=plant_disease_detection
JWT_SECRET=replace-with-long-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
MODEL_PATH=../ml-service/saved_models/best_model.keras
LABELS_PATH=../ml-service/saved_models/labels.json
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_MB=10
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
DEBUG=false
```

The frontend uses:

```text
VITE_API_BASE_URL=http://localhost:8000
```

## 15. Deployment Considerations

### Security

- Use a strong `JWT_SECRET` in production.
- Serve all traffic over HTTPS.
- Store JWTs carefully. For higher security, consider HttpOnly cookies instead of local storage.
- Keep access tokens short-lived and use refresh tokens for session continuity.
- Validate uploaded file type, size, and content.
- Restrict CORS origins to trusted frontend domains.
- Do not expose stack traces in production responses.
- Store secrets in a managed secret store or deployment platform environment variables.

### Error Handling

The backend uses centralized exception handlers for:

- Validation errors: 400
- Unauthorized access: 401
- Forbidden access: 403
- Missing resources: 404
- Duplicate resources: 409
- Unexpected server failures: 500

Responses follow a consistent shape:

```json
{
  "success": false,
  "message": "Validation error",
  "detail": []
}
```

### Logging

Backend logging should include:

- Startup and MongoDB connection status
- Authentication failures without sensitive data
- Upload validation failures
- Prediction failures
- Model loading events
- Unexpected exceptions

ML logging should include:

- Dataset split summary
- Training start and end
- Epoch metrics through TensorBoard
- Evaluation metrics
- Model export metadata

### Scalability

For larger production usage:

- Move uploaded images to object storage such as S3, Azure Blob Storage, or GCS.
- Serve static files through a CDN.
- Run MongoDB as a managed cluster.
- Use a background worker for heavy prediction jobs if latency becomes high.
- Keep TensorFlow model loading process-local and cached.
- Consider a separate ML inference service if GPU acceleration or horizontal scaling is required.
- Add rate limiting at API gateway or middleware level.
- Add request tracing and metrics with Prometheus, OpenTelemetry, or cloud monitoring.

### Deployment Topology

```text
Browser
  |
  v
CDN / Static Hosting for React
  |
  v
API Gateway / Reverse Proxy
  |
  v
FastAPI Backend Containers
  |
  +--> MongoDB Managed Cluster
  |
  +--> Object Storage for uploads
  |
  +--> ML Model Artifacts or Dedicated ML Inference Service
```

### CI/CD Recommendations

- Run frontend lint and build on every pull request.
- Run backend `compileall` and API unit tests.
- Run ML service syntax checks and lightweight import checks.
- Store trained model artifacts in a model registry or versioned storage.
- Use environment-specific `.env` values.
- Add health checks for backend and model artifact readiness.

## 16. Current Operational Readiness

The application code is implemented, but ML runtime readiness depends on real model artifacts.

To produce production ML artifacts:

```powershell
cd ml-service
python preprocessing/split_dataset.py
python training/train.py --architecture efficientnetb0
python utils/artifact_validator.py
```

The validator reports whether the system is ready for:

- Training
- Inference
- Backend prediction requests

The backend prediction API requires:

- `ml-service/saved_models/best_model.keras`
- `ml-service/saved_models/labels.json`
- MongoDB running and reachable
- Valid JWT access token

## 17. Summary

This system combines a React frontend, FastAPI backend, MongoDB database, secure JWT authentication, file upload storage, and a TensorFlow/Keras ML pipeline. The backend is the orchestration layer that validates requests, manages users, stores predictions, and invokes the trained model. The ML service owns dataset preparation, model training, evaluation, inference artifacts, and explainability. The frontend provides a user-friendly workflow for upload, diagnosis, history, dashboard analytics, and profile management.

For a new engineer, the most important mental model is:

```text
Frontend handles interaction.
Backend handles security, orchestration, persistence, and API contracts.
ML service produces and serves model-ready artifacts.
MongoDB stores users, disease knowledge, and prediction history.
Uploads store original, processed, and prediction-derived image files.
```
