from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    @abstractmethod
    def dumps(self, obj: any) -> str:
        """ this method is too abstract to understand. """
    @abstractmethod
    def dump(self, obj: any, file_path: str):
        """ this method is too abstract to understand. """
    @abstractmethod
    def loads(self, source: str) -> any:
        """ this method is too abstract to understand. """
    @abstractmethod
    def load(self, file_path: str) -> any:
        """ this method is too abstract to understand. """