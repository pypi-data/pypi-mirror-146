import logging


class Abstract:

    def __init__(self):
        self.__logger = None
        pass

    @property
    def logger(self) -> logging:
        return self.__logger

    @logger.setter
    def logger(self, value: logging):
        self.__logger = value
