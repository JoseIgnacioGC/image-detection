import cv2
import numpy as np
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
import torch

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"
processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

def segment_person(image: np.ndarray) -> np.ndarray:
    input_image = cv2.resize(image, (512, 512))

    inputs = processor(images=input_image, return_tensors="pt")

    device = torch.device("cuda")
    model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    mask = outputs.logits.argmax(dim=1).squeeze().cpu().numpy()

    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    red_overlay = np.zeros_like(image, dtype=np.uint8)
    red_overlay[mask_resized == 12] = [0, 0, 255]  # Clase 12 = persona

    segmented_image = cv2.addWeighted(image, 1, red_overlay, 0.5, 0)

    return segmented_image
