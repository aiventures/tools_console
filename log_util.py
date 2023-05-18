""" log util to bootstrap logging """
import logging
from logging.config import dictConfig
import os
import json
from tools_console.persistence import Persistence

logger = logging.getLogger(__name__)

class LoggingConfig(object):
    """ Logging Config """

    def __init__(self,fp:str="./config/config_log.json") -> None:
        """ Constructor
        Args:
            fp (str, optional): PAth to logging Config json. Defaults to "./config/config_log.json".
        """
        self._config = LoggingConfig.read_config(fp)

    @property
    def config(self):
        """ config dict """
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def get_logger_configs(self):
        """ logger configs """
        return self._config["loggers"].keys()

    def get_handler_configs(self):
        """ handler configs """
        return self._config["handlers"].keys()

    def get_formatter_configs(self):
        """ formatter configs """
        return self._config["formatters"].keys()

    @staticmethod
    def read_config(fp:str)->dict:
        """ read config file for logging
        Args:

        Returns:
            dict: config file
        """
        logger.info("Read Log Config file: %s",fp)
        if not os.path.isfile(fp):
            logger.error("Log Info file %s not found",fp)
            return None
        config = Persistence.read_json(fp)
        logger.debug("Config file: %s",str(config))
        return config

    def configure(self):
        """ set up logging config, needs to be done first in code when all setup was done """
        if self._config:
            dictConfig(self._config)
        else:
            logger.error("Logging configuration not set")

if __name__ == "__main__":
    my_config = LoggingConfig()
    config_dict = my_config.config
    print("### CONFIG DICT ###")
    print(json.dumps(config_dict, indent=4,sort_keys=False,ensure_ascii=True))
    print(f"LOGGERS: {my_config.get_logger_configs()}")
    # do some dict adjustments
    # activate
    my_config.configure()
    # logging.getLogger().setLevel(logging.INFO)

    logger.debug("TEST LOGGER DEBUG")
    logger.info("TEST LOGGER INFO")
    logger.warning("TEST LOGGER WARN")
    logger.error("TEST LOGGER ERROR")

