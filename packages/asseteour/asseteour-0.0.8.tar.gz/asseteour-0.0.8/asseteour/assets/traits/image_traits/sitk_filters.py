
import io
import json
from enum import Enum

import SimpleITK as sitk
# import full filters from the module.
# the filter object would be auto casted through eval
from canvas_app.sitk_image_filters import (DenoisingVolumeImageFilter,
                                           DiscreteGaussianImageFilter,
                                           EnhanceVolumeImageFilter,
                                           UnsharpMaskImageFilter,
                                           SyngularVolumeImageFilter)
from pydantic import Field, validator
from compipe.utils.logging import logger
from utils.utilities import validate_func_param

from ..array_item import BaseArrayItem


class SITKFilterItems(Enum):
    DiscreteGaussian = DiscreteGaussianImageFilter.__name__
    UnsharpMask = UnsharpMaskImageFilter.__name__
    EnhanceVolumeImage = EnhanceVolumeImageFilter.__name__
    DenoisingVolumeImage = DenoisingVolumeImageFilter.__name__
    SyngularVolumeImage = SyngularVolumeImageFilter.__name__


class SITKFilter(BaseArrayItem):

    name: SITKFilterItems = Field(...,
                                  title='SimpleITK Image Filter Name',
                                  description='The ImageFilter module contains '
                                  'definitions for a pre-defined set of filters.\n'
                                  '>DiscreteGaussianImageFilter: Blurs an image '
                                  'by separable convolution with discrete gaussian '
                                  'kernels. This filter performs Gaussian blurring '
                                  'by separable convolution of an image and a discrete '
                                  'Gaussian operator (kernel).\n'
                                  '>UnsharpMaskImageFilter: Edge enhancement filter.\n')

    param: dict = Field(...,
                        title='Filter Argument',
                        description='Represent volume image filter parameters. '
                        'Refer to the module "sitk_image_filters" for'
                        'learning the usage of each parameters.')

    @property
    def filter_name(self):
        return self.name.value  # pylint: disable=no-member

    def apply(self, img):
        img = sitk.Cast(img, sitk.sitkFloat32)
        img = eval(f'{self.filter_name}')(img=img, **self.param)
        return sitk.Cast(img, sitk.sitkFloat32)

    @validator('param')
    def is_valid_filter_param(cls, param, values, **kwargs):  # pylint: disable=no-self-argument
        if not values.get("name"):
            raise ValueError("unexpected filter name, please add new filters in class 'SITKFilterItems'")
        else:
            filter_name = values.get("name").value
            validate_func_param(eval(filter_name), param, ignore=['img', 'output'])
        return param

    class Config:
        schema_extra = {
            'examples': [{
                'enable': True,
                'name': SITKFilterItems.UnsharpMask,
                'param': {
                    "amount": 2,
                    "sigmas": 1
                }
            },
                {
                "name": SITKFilterItems.EnhanceVolumeImage,
                "param": {
                    "model": "models-cunet",
                    "sr_factor": 0,
                    "scale": 2
                }
            },
                {
                "name": SITKFilterItems.DenoisingVolumeImage,
                "param": {
                    "level": 15
                }
            }]
        }
