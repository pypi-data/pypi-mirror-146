import io
import json
from enum import Enum

from canvas_app.image_utils import image_bytes_loader
from PIL import Image, ImageFilter
from pydantic import Field, validator
from compipe.utils.mime_types import GMimeTypes

from ..array_item import BaseArrayItem
from compipe.utils.logging import logger

# EVAL FUNCTION NAME LISTS
IMAGE_FILTER = ImageFilter.__name__.split(".")[-1]


class PILFilters(Enum):
    GaussianBlur = 'GaussianBlur'
    BoxBlur = 'BoxBlur'
    UnsharpMask = 'UnsharpMask'
    Color3DLUT = 'Color3DLUT'
    Kernel = 'Kernel'
    RankFilter = 'RankFilter'
    MedianFilter = 'MedianFilter'


class GFilter(BaseArrayItem):
    name: PILFilters = Field(PILFilters.GaussianBlur,
                             title='PIL ImageFilter Name',
                             description='The ImageFilter module contains '
                             'definitions for a pre-defined set of filters, '
                             'which can be be used with the Image.filter() method.')

    param: dict = Field({'radius': 0},
                        title='Filter Argument',
                        description='Represent the arguments to be applied '
                        'with a specific filter')

    @property
    def filter_name(self):
        return self.name.value  # pylint: disable=no-member

    def apply(self, image, mime_type=GMimeTypes.WEBP):
        is_bytes_data = isinstance(image, bytes)
        if is_bytes_data:
            image = Image.open(io.BytesIO(image))
        image = image.filter(eval(f'{IMAGE_FILTER}.{self.filter_name}')(**self.param))
        return image_bytes_loader(data=image, ext=mime_type.name) if is_bytes_data else image

    @validator('param')
    def is_valid_filter_param(cls, v, values, **kwargs):  # pylint: disable=no-self-argument

        if not values.get("name"):
            raise ValueError("unexpected filter name, please add new filters in class 'PILFilters'")
        else:
            filter_name = values.get("name").value

            try:
                eval(f'{IMAGE_FILTER}.{filter_name}')(**v)
            except Exception as e:
                logger.error(e)
                raise ValueError(f'must specify valid ImageFilter arguments. '
                                 f'Name: {filter_name}, Argument:{json.dumps(v)} '
                                 'https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html')
        return v

    class Config:
        schema_extra = {
            'examples': [{
                'enable': True,
                'name': PILFilters.GaussianBlur,
                'param': {
                    'radius': 10
                }
            }]
        }
