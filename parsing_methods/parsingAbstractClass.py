from abc import ABCMeta, abstractmethod, abstractproperty, ABC


class Parsing(ABC):

    @abstractmethod
    def parsing(self):
        """Основной метод для парсинга"""

    @abstractmethod
    def get_name_class(self):
        """Метод для получения имени класса"""
