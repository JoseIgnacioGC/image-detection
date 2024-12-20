from src.utils import DATA_DIR
from src.img_captioning.utils import Img

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

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


conversation = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {
                "text": 'Is there a violent scene in the image? (even if is in a cellphone image and ignoring thumps up) Answer using the following format (2 elements a str and an int): ["descripcion de la imagen en español", how much violent there are in the image? (on a scale from 1 to 10)]',
            },
        ],
    }
]

text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)


def generate_model_response(img: Img) -> str:
    inputs = processor(
        text=[text_prompt], images=[img], padding=True, return_tensors="pt"
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
