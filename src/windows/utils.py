from cv2.typing import MatLike
from PIL import Image
import cv2


def calculate_cv2_img_proportional_height(image: MatLike, target_width: int) -> int:
    height, width = image.shape[:2]
    aspect_ratio = height / width
    return int(target_width * aspect_ratio)


def calcualte_pil_img_proportional_height(image: Image.Image, target_width: int) -> int:
    width, height = image.size
    aspect_ratio = height / width
    return int(target_width * aspect_ratio)


def cv2_to_pil(cv2_img: MatLike) -> Image.Image:
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img)
    return pil_img
