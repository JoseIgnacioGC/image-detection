from src.utils import DATA_DIR

import json
from datetime import datetime
from typing import Any
from dataclasses import dataclass


@dataclass
class ModelResponse:
    image_description: str
    is_a_crime: bool


def process_model_response(model_response_raw: str) -> ModelResponse:
    try:
        parsed_list: list[Any] = json.loads(model_response_raw)

        if len(parsed_list) != 2:
            raise ValueError("Invalid model response structure")

        image_description = parsed_list[0]
        is_a_crime = parsed_list[1]

        if (
            not isinstance(image_description, str)
            or image_description == ""
            or not isinstance(is_a_crime, bool)
        ):
            raise ValueError("Invalid data types in model response")

        model_res = ModelResponse(image_description, is_a_crime=is_a_crime)
        with open(DATA_DIR / "logs.txt", "a") as f:
            f.write(
                f"{str(model_res.__dict__)} - {datetime.now().replace(microsecond=0)}\n"
            )
        return model_res

    except:
        with open(DATA_DIR / "error_response_logs.txt", "a") as f:
            f.write(f"{model_response_raw} - {datetime.now().replace(microsecond=0)}\n")
        return ModelResponse("", is_a_crime=False)
