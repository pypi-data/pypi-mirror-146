from abc import ABCMeta, abstractmethod
from typing import Dict
from pydantic import PrivateAttr


class BaseAssetWrapper(PrivateAttr, metaclass=ABCMeta):

    @abstractmethod
    @classmethod
    def parse(cls, payload: Dict):
        pass

    @abstractmethod
    @classmethod
    def schema_json(cls, indent=4):
        pass
