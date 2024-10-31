from src.img_captioning.utils import IMAGE_CONDITION

from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers.modeling_utils import PreTrainedModel
from PIL import Image


def charge_model() -> dict[str, BlipProcessor | PreTrainedModel]:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
    return {"processor": processor, "model": model}


def generate_image_description(
    raw_image: Image.Image, processor: BlipProcessor, model: PreTrainedModel
) -> str:
    inputs = processor(raw_image, IMAGE_CONDITION, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=100)
    description: str = processor.decode(out[0], skip_special_tokens=True)

    return description
