from functools import cached_property
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from model.domain import FEATURE_NAMES, TARGET_NAMES

MODEL_DIR_PATH = Path(__file__).parent.parent / "models"


class ModelManager:
    """Helper class for managing models that cover all targets"""

    def __init__(self, model_name: str):
        self.model_name = model_name

    def _load_model(self, for_target: str) -> Pipeline:
        model_path = MODEL_DIR_PATH / f"{self.model_name}_{for_target}.pkl"

        return joblib.load(model_path)

    @cached_property
    def class_to_model(self):
        return {target: self._load_model(target) for target in TARGET_NAMES}

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        result_df = data.copy()

        for target in TARGET_NAMES:
            result_df[target] = self.predict_single(data, target)

        return result_df

    def predict_single(self, data: pd.DataFrame, target: str) -> pd.Series:
        return self.class_to_model[target].predict(data[FEATURE_NAMES])
