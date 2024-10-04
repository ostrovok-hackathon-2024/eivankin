import sys
from pathlib import Path

import pandas as pd
import typer

from model.domain import AvailableModels
from model.manager import ModelManager

app = typer.Typer()


@app.command()
def run_inference(
    input_path: Path = typer.Option(..., "--content", help="A path to rates CSV file"),
    model: AvailableModels = AvailableModels.LINEAR_SVC,
):
    df = pd.read_csv(input_path).fillna("undefined")

    manager = ModelManager(model)
    result_df = manager.predict(df)

    result_df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    app()
