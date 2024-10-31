from dataclasses import dataclass

from transformers import BlipProcessor
from transformers.modeling_utils import PreTrainedModel

from PIL.Image import Image


@dataclass
class ProcessorModel:
    processor: BlipProcessor
    model: PreTrainedModel


@dataclass
class ImageDescriptionParams:
    raw_image: Image
    ProcessorModel: ProcessorModel


IMAGE_CONDITION = "a photography of"
