from src.img_captioning.utils import (
    ImageDescriptionParams,
    ProcessorModel,
)

from random import choice

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


def charge_model() -> ProcessorModel:
    model = None
    if torch.cuda.is_available():
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large", torch_dtype=torch.float16
        )
        model = model.to("cuda")
    else:
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large"
        )

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

    return ProcessorModel(processor=processor, model=model)


fake_response = (
    ('{"image_description": "1 a person with  long hair", "is_a_crime": false}'),
    ('{"image_description": "2 a person with  long hair", "is_a_crime": false}'),
    ('{"image_description": "3 a person with  long hair", "is_a_crime": false}'),
    ('{"image_description": "1 a person with a gun", "is_a_crime": true}'),
    ('{"image_description": "2 a person with a gun", "is_a_crime": true}'),
    ('{"image_description": "3 a person with a gun", "is_a_crime": true}'),
    ('{"image_description": "5 a person with a knife", "is_a_crime": true}'),
    ('{"image_description": "bad format", "is_a_crime": 1234}'),
    ('{"image_description": "2 bad format", "is_a_crime": 1234}'),
    ('{"image_description: (23, 34), "is_a_crime": (32, 53)}'),
    ('{"image_description": "bad format", "is_a_crime": true'),
)


def generate_image_description(params: ImageDescriptionParams) -> str:
    _processor = params.ProcessorModel.processor
    _model = params.ProcessorModel.model

    # inputs = processor(params.raw_image, IMAGE_CONDITION, return_tensors="pt")
    # if torch.cuda.is_available():
    #     inputs = inputs.to("cuda", torch.float16)

    # out = model.generate(**inputs)  # max_new_tokens=100

    # description = cast(str, processor.decode(out[0], skip_special_tokens=True))

    # structure:  {"image_description": "your description", "is_a_crime": true/false}
    return choice(fake_response)
