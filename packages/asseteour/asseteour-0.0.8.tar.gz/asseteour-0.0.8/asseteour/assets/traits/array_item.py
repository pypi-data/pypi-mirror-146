import json
import math
from abc import ABCMeta, abstractmethod
from enum import Enum

from pydantic import BaseModel, Field, validator


class BaseArrayItem(BaseModel):

    name: str = Field(...,
                      title='Item identity',
                      description='Represent the unique item key name')

    is_enabled: bool = Field(True,
                             title='Enable flag',
                             description='Represent the available states.')
