from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers.modeling_utils import PreTrainedModel

IMAGE_CONDITION = "a photography of"


def get_processor_and_model() -> tuple[BlipProcessor, PreTrainedModel]:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
    return (processor, model)


def generate_image_description(
    processor: BlipProcessor, model: PreTrainedModel, raw_image: Image.Image
) -> str:

    # conditional image captioning
    inputs = processor(raw_image, IMAGE_CONDITION, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    return description

    # unconditional image captioning
    # inputs = processor(raw_image, return_tensors="pt")
    # out = model.generate(**inputs)
    # print(processor.decode(out[0], skip_special_tokens=True))
