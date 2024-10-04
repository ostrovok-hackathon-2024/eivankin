from enum import StrEnum

TARGET_NAMES = [
    "class",
    "quality",
    "bathroom",
    "bedding",
    "capacity",
    "club",
    "balcony",
    "view",
]
FEATURE_NAMES = ["rate_name"]


class AvailableModels(StrEnum):
    LINEAR_SVC = "svc_pipeline"
    RIDGE_CLASSIFIER = "ridge_pipeline"
