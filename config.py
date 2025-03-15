import yaml
from loguru import logger
from utils.log_utils import LoguruLogger, LoguruSettings


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Server
HOST = config["app"]["host"]
PORT = config["app"]["port"]

# Logging
LEVEL = config["logging"]["level"]
FILE_PATH = config["logging"]["file_path"]

# Dataset
MIN_TEXT_LENGTH = config["suggestions"]["min_text_length"]

logger = LoguruLogger()

file_config = LoguruSettings.file_config(
    filepath=FILE_PATH,
    level=LEVEL,
    retention="10 days",
    serialize=False
)
logger.add_sink(file_config)

console_config = LoguruSettings.console_config(level="DEBUG")
logger.add_sink(console_config)