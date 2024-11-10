from dataclasses import dataclass
from typing import TYPE_CHECKING
from PIL.Image import Image

if TYPE_CHECKING:
    from transformers.modeling_utils import PreTrainedModel
    from transformers import BlipProcessor


@dataclass
class ProcessorModel:
    processor: "BlipProcessor"
    model: "PreTrainedModel"


@dataclass
class ImageDescriptionParams:
    raw_image: Image
    ProcessorModel: ProcessorModel


IMAGE_CONDITION = "a photography of"
