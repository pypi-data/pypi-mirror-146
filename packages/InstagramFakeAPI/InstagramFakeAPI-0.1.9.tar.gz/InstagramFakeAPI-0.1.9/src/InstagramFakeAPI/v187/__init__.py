import logging

from .mixin.action import InstagramCustom


class Client(InstagramCustom):
    logger = logging.getLogger("src")

    def __init__(self, logger):
        InstagramCustom.__init__(self,logger)
