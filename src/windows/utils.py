from PIL import Image


def calculate_proportional_height(pil_img: Image.Image, target_width: int):
    width, height = pil_img.size
    aspect_ratio = height / width
    return int(target_width * aspect_ratio)
