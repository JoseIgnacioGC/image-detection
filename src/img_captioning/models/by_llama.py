import torch
from src.img_captioning.utils import (
    ImageDescriptionParams,
    ProcessorModel,
)

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

# https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct Accurate
# https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct Less accurate

"""
    ERROR: ValueError: You are trying to offload the whole model to the disk. Please use the `disk_offload` function instead.
    - https://discuss.huggingface.co/t/valueerror-you-are-trying-to-offload-the-whole-model-to-the-disk-please-use-the-disk-offload-function-instead/66687/6
    - https://medium.com/@sridevi17j/resolving-valueerror-you-are-trying-to-offload-the-whole-model-to-the-disk-70d4e8138797
    - https://github.com/huggingface/accelerate/issues/2129
    - https://stackoverflow.com/questions/77701433/valueerror-you-are-trying-to-offload-the-whole-model-to-the-disk-please-use-th
"""


def charge_model() -> ProcessorModel:
    model = None
    if torch.cuda.is_available():
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
            device_map="auto",
            offload_folder=r"./../../../resources/offload",
            # offload_state_dict=True,
        )
    else:
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype="auto",
            device_map="auto",
            offload_folder=r"./../../../resources/offload",
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
