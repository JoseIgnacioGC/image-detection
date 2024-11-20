from time import sleep
from typing import Any

import random

from src.async_utils import run_in_background

valid_crime_responses = (
    '["Person pointing gun at camera", true]',
    '["Phone showing robbery video", true]',
    '["Security camera footage of shoplifting", true]',
    '["Person breaking car window", true]',
    '["Graffiti on wall in progress", true]',
    '["Person in ski mask entering window", true]',
    '["Phone showing illegal drug deal", true]',
    '["Person picking door lock", true]',
    '[should not cause an error, "True"]',
    '["Phone displaying bank robbery", true]',
)

valid_normal_responses = (
    '["Empty parking lot at night", false]',
    '["Kids playing in park", false]',
    '["Peaceful protest march", false]',
    '["Students studying in library", false]',
    '["Couple walking dog at night", false]',
    '["Security guard on patrol", false]',
)


invalid_responses = (
    "Person pointing gun at camera, True",
    '{"desc": "Crime scene", "crime": TRUE}',
    '["Kids playing in park", 422]',
    "[42, FALSE]",
    "",
    '[false, "Kids playing in park"]',
    "null",
    "[Multiple, true, elements]",
    '"Security camera footage of shoplifting", true]',
    "[null, True]",
    "[]",
)


def get_response() -> str:
    # return random.choice(valid_crime_responses)
    return random.choice(valid_crime_responses + valid_normal_responses)
    return random.choice(
        valid_crime_responses + valid_normal_responses + invalid_responses
    )


@run_in_background
def generate_model_response(img: Any):
    sleep(1)
    return get_response()


def initialize_model_generator(processor_option: Any):
    return generate_model_response
