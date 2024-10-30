from dataclasses import dataclass

from transformers import BlipProcessor
from transformers.modeling_utils import PreTrainedModel
from PIL.Image import Image


@dataclass
class ImageDescriptionParams:
    raw_image: Image
    processor: BlipProcessor
    model: PreTrainedModel
