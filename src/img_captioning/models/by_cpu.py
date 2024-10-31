from src.img_captioning.utils import (
    IMAGE_CONDITION,
    ImageDescriptionParams,
    ProcessorModel,
)

from transformers import BlipProcessor, BlipForConditionalGeneration


def charge_model() -> ProcessorModel:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
    return {"processor": processor, "model": model}


def generate_image_description(params: ImageDescriptionParams) -> str:
    inputs = params.processor(params.raw_image, IMAGE_CONDITION, return_tensors="pt")
    out = params.model.generate(**inputs, max_new_tokens=100)
    description: str = params.processor.decode(out[0], skip_special_tokens=True)

    return description
