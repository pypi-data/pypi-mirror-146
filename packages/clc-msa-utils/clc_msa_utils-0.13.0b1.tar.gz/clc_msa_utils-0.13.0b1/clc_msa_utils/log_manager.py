import logging
import datetime
import json_log_formatter

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra['message'] = message

        # Include builtins
        extra['severity'] = record.levelname
        extra['source'] = record.name
        extra['pathname'] = record.pathname
        extra['lineno'] = record.lineno
        extra['func'] = record.funcName

        if 'time' not in extra:
            extra['time'] = datetime.datetime.utcnow()
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra

formatter = CustomisedJSONFormatter()
json_handler = logging.FileHandler("/dev/stdout")
json_handler.setFormatter(formatter)

# This redirects warnings to be logged, so that they are logged as json with the correct warning severity
# However, warnings that are captured by other means may need to turn this off before hand (and then back on afterwards)
logging.captureWarnings(True)
logger = logging.getLogger()
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

class LogManager:
    def __init__(self,
                 kv_store):
        # logger for this class
        self._logger = logging.getLogger("LogManager")

        self._kv_store = kv_store
        self._configure_logging(None, kv_store.get_dict(default={}))
        self._kv_store.on_reload(self._configure_logging)

    def _configure_logging(self, old_config, new_config):
        self._logger.debug("BEGIN _configure_logging")

        if not old_config or not old_config == new_config:
            self._logger.debug("Configuration changed, configuring logging...")
            logger = logging.getLogger()
            try:
                if 'logging_level' in new_config:
                    numeric_level = getattr(logging, new_config.get('logging_level'))
                    logger.setLevel(numeric_level)
                else:
                    logger.setLevel(logging.INFO)
            except:
                self._logger.warning("Invalid level, {1}, for root logging configuration."
                                     .format("logging_level", new_config.get('logging_level')))

            # Specific logger configuration
            if 'logging_config' in new_config and type(new_config.get('logging_config')) is dict:
                self._logger.debug("logging_config found.")
                logging_config = new_config.get('logging_config')

                for log_name in logging_config:
                    logger = logging.getLogger(log_name)
                    current_logging_config = logging_config.get(log_name)
                    self._logger.debug("Configuration for {0} is {1}.".format(log_name, str(current_logging_config)))

                    if type(current_logging_config) is str:
                        self._logger.debug("Configuring logger for {0}..."
                                           .format(log_name))
                        try:
                            numeric_level = getattr(logging, current_logging_config)
                            self._logger.debug("Configuring logging level to {0} for {1}..."
                                               .format(str(numeric_level), log_name))
                            logger.setLevel(numeric_level)
                        except:
                            self._logger.warning("Invalid level, {1}, for {0} logging configuration."
                                                 .format(log_name, current_logging_config))
            else:
                self._logger.debug("logging_config NOT found.")
        else:
            self._logger.debug("Configuration unchanged.")
        self._logger.debug("END _configure_logging")
