"""Implement the filters of enhancing 2D images.
"""
import io
import json
from enum import Enum
from inspect import getargspec, getfullargspec

import SimpleITK as sikt
from cv2 import dft
# import full filters from the module.
# the filter object would be auto casted through eval
from canvas_app.Image_enhance_filters import (ESRGANImageFilter,
                                              SwinIRImageFilter,
                                              Waifu2xImageFilter,
                                              SyngularImageFilter)
from pydantic import Field, validator
from compipe.utils.logging import logger
from utils.utilities import validate_func_param

from ..array_item import BaseArrayItem


class ImageFilterItems(Enum):
    Waifu2xImage = Waifu2xImageFilter.__name__
    ESRGANImage = ESRGANImageFilter.__name__
    SwinIRImage = SwinIRImageFilter.__name__
    SyngularImage = SyngularImageFilter.__name__


class EnhanceImageFilter(BaseArrayItem):

    name: ImageFilterItems = Field(...,
                                   title='2D Image enhancement filter name.')

    param: dict = Field(...,
                        title='Filter Argument',
                        description='Represent image filter function parameters. '
                        'Refer to the module "Image_enhance_filters.py" for'
                        'learning the usage of each paramters.')

    @property
    def filter_name(self):
        return self.name.value  # pylint: disable=no-member

    def apply(self, img):
        eval(f'{self.filter_name}')(img=img, **self.param)

    @validator('param')
    def is_valid_filter_param(cls, param, values, **kwargs):  # pylint: disable=no-self-argument
        if not values.get("name"):
            raise ValueError("unexpected filter name, please add new filters in class 'Image_enhance_filters'")
        else:
            filter_name = values.get("name").value
            validate_func_param(eval(filter_name), param, ignore=['img', 'output'])
        return param

    class Config:
        schema_extra = {
            'examples': [{
                'enable': True,
                'name': ImageFilterItems.Waifu2xImage,
                'param': {
                    "sr_factor": 1,
                    "scale": 1
                }
            }]
        }
