import cv2
from cv2.typing import MatLike
from PIL import Image

def convert_opencv_to_pil(cv_image: MatLike) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))