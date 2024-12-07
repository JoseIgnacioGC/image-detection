import cv2
import numpy as np
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
from PIL import Image
import torch

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"
processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

def segment_person(image: np.ndarray) -> np.ndarray:

    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    inputs = processor(images=pil_image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    mask = outputs.logits.argmax(dim=1).squeeze().cpu().numpy()

    if mask is None or mask.size == 0:
        raise ValueError("La máscara generada está vacía o no es válida.")

    if image is None or image.shape[0] == 0 or image.shape[1] == 0:
        raise ValueError("La imagen de entrada es inválida.")

    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    red_overlay = np.zeros_like(image, dtype=np.uint8)
    red_overlay[mask_resized == 12] = [0, 0, 255]  # Clase 12 en ADE20K corresponde a "persona"

    segmented_image = cv2.addWeighted(image, 1, red_overlay, 0.5, 0)

    return segmented_image