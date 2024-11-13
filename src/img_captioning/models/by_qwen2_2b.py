from src.img_captioning.utils import (
    ImageDescriptionParams,
    ProcessorModel,
)
from src.utils import DATA_DIR

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor


def charge_model() -> ProcessorModel:
    model_name = "Qwen/Qwen2-VL-2B-Instruct"
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        offload_folder=DATA_DIR / "offload",
    )

    min_pixels = 256 * 28 * 28
    max_pixels = 1280 * 28 * 28
    processor = AutoProcessor.from_pretrained(
        model_name, min_pixels=min_pixels, max_pixels=max_pixels
    )

    return ProcessorModel(processor=processor, model=model)


conversation = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {
                "type": "text",
                "text": 'Is a crime being committed in the following image (count even if it\'s an image of a phone). Answer using the format ["img description", true/false if is a crime].',
            },
        ],
    }
]


def generate_image_description(params: ImageDescriptionParams) -> str:
    processor = params.ProcessorModel.processor
    model = params.ProcessorModel.model
    image = params.raw_image

    text_prompt = processor.apply_chat_template(
        conversation, add_generation_prompt=True
    )

    inputs = processor(
        text=[text_prompt], images=[image], padding=True, return_tensors="pt"
    ).to("cuda")

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=50)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    model_response = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    return model_response[0]
