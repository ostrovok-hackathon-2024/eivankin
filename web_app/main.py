import os
from contextlib import asynccontextmanager
from typing import Annotated, List

import pandas as pd
from annotated_types import Len
from fastapi import Depends, FastAPI
from pydantic import BaseModel, StringConstraints

from model.manager import ModelManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_name = os.getenv("MODEL_NAME", "svc_pipeline")
    app.model_manager = ModelManager(model_name)
    if len(app.model_manager.class_to_model) == 0:
        raise RuntimeError("No model found")
    yield


app = FastAPI(lifespan=lifespan)


def get_model_manager() -> ModelManager:
    return app.model_manager


Query = Annotated[str, StringConstraints(min_length=1, max_length=500)]

QueryList = Annotated[List[str], Len(min_length=2, max_length=200)]


class SingleInference(BaseModel):
    text: Query


class BatchInference(BaseModel):
    texts: QueryList


@app.post("/infer/single")
async def infer_single(
    inference: SingleInference, model_manager: ModelManager = Depends(get_model_manager)
):
    prediction = model_manager.predict(
        pd.DataFrame([inference.text], columns=["rate_name"])
    )
    return {"prediction": prediction.to_dict(orient="records")}


@app.post("/infer/batch")
async def infer_batch(
    inference: BatchInference, model_manager: ModelManager = Depends(get_model_manager)
):
    predictions = model_manager.predict(
        pd.DataFrame(inference.texts, columns=["rate_name"])
    )
    return {"predictions": predictions.to_dict(orient="records")}
