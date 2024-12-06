from time import sleep
from typing import Any

import random

from src.async_utils import run_in_background

valid_crime_responses = (
    '["Person pointing gun at camera", 5]',
    '["Phone showing robbery video", 10]',
    '["Security camera footage of shoplifting", 6]',
    '["Person breaking car window", 7]',
    '["Graffiti on wall in progress", 5]',
    "[should not cause an error, 6]",
    '["Phone displaying bank robbery", 8]',
)

valid_normal_responses = (
    '["Empty parking lot at night", 1]',
    '["Kids playing in park", 3]',
    '["Peaceful protest march", 2]',
    '["Students studying in library", 1]',
    '["Couple walking dog at night", 4]',
    '["Security guard on patrol", 0]',
)


invalid_responses = (
    '["Person in ski mask entering window", true]',
    '["Phone showing illegal drug deal", true]',
    '["Person picking door lock", true]',
    "Person pointing gun at camera, True",
    '{"desc": "Crime scene", "crime": TRUE}',
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
    return random.choice(valid_crime_responses)
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
