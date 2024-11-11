from src.utils import RESOURCES_DIR

import json
from datetime import datetime
from typing import Any
from dataclasses import dataclass, fields


@dataclass
class ModelResponse:
    image_description: str
    is_a_crime: bool


def process_model_response(
    model_response_raw: str, image_description: str
) -> ModelResponse | None:
    try:
        parsed_model_res: dict[Any, Any] = json.loads(model_response_raw)
        model_fields: dict[str, Any] = {
            field.name: field.type for field in fields(ModelResponse)
        }
        if not all(
            key in parsed_model_res
            and isinstance(parsed_model_res[key], model_fields[key])
            for key in model_fields
        ):
            raise ValueError("Invalid model response structure")

        model_res = ModelResponse(**parsed_model_res)
        if image_description == model_res.image_description:
            return None
        with open(RESOURCES_DIR / "logs.txt", "a") as f:
            f.write(f"{model_response_raw} - {datetime.now().replace(microsecond=0)}\n")
        return model_res

    except:
        with open(RESOURCES_DIR / "error_response_logs.txt", "a") as f:
            f.write(f"{model_response_raw} - {datetime.now().replace(microsecond=0)}\n")
