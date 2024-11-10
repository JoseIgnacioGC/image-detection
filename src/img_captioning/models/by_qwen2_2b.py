import torch
from src.img_captioning.utils import (
    ImageDescriptionParams,
    ProcessorModel,
)

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

from utils import RESOURCES_DIR


def charge_model() -> ProcessorModel:
    model = None
    if torch.cuda.is_available():
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
            device_map="auto",
            offload_folder=RESOURCES_DIR / "offload",
            # offload_state_dict=True,
        )
    else:
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype="auto",
            device_map="auto",
            offload_folder=RESOURCES_DIR / "offload",
        )

    min_pixels = 256 * 28 * 28
    max_pixels = 1280 * 28 * 28
    processor = AutoProcessor.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels
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
                "text": "is a crime taking place in the following image?",
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
    )
    if torch.cuda.is_available():
        inputs = inputs.to("cuda")

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=50)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    description = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    return description
