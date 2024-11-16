from typing import Any

import random

valid_responses = (
    '["Person pointing gun at camera", true]',
    '["Empty parking lot at night", false]',
    '["Phone showing robbery video", true]',
    '["Kids playing in park", false]',
    '["Security camera footage of shoplifting", true]',
    '["Person breaking car window", true]',
    '["Graffiti on wall in progress", true]',
    '["Person in ski mask entering window", true]',
    '["Peaceful protest march", false]',
    '["Phone showing illegal drug deal", true]',
    '["Students studying in library", false]',
    '["Person picking door lock", true]',
    '["Couple walking dog at night", false]',
    '["Security guard on patrol", false]',
    '[should not cause an error, "True"]',
    '["Phone displaying bank robbery", true]',
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
    return random.choice(valid_responses + invalid_responses)


def generate_model_response(processor_option: Any, image: Any):
    return get_response()
