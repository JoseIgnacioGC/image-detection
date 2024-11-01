from typing import cast
from src.img_captioning.utils import (
    IMAGE_CONDITION,
    ImageDescriptionParams,
    ProcessorModel,
)

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

def charge_model() -> ProcessorModel:
    processor = cast(
        BlipProcessor,
        BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large"),
    )
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large", torch_dtype=torch.float16
    ).to("cuda")
    return ProcessorModel(processor=processor, model=model)

def generate_image_description(params: ImageDescriptionParams) -> str:
    processor = params.ProcessorModel.processor

    model = params.ProcessorModel.model

    inputs = processor(params.raw_image, IMAGE_CONDITION, return_tensors="pt").to(
        "cuda", torch.float16
    )
    out = model.generate(**inputs)
    description = cast(str, processor.decode(out[0], skip_special_tokens=True))

    return description