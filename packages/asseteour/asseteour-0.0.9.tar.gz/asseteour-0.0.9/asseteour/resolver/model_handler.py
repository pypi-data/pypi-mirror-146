from abc import ABCMeta, abstractmethod


class BaseAsset(metaclass=ABCMeta):

    @abstractmethod
    def parse(self):
        pass
