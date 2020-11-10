import logging
import configparser
from src.bot import Bot
import time


if __name__ == "__main__":
    # config file parser initialization
    config = configparser.ConfigParser()
    config.read("config.ini")

    # custom logging format
    logging.basicConfig(
        level=logging.DEBUG
        if config["OTHER"].getboolean("DEBUG", fallback=False) == True
        else logging.INFO,
        format="%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s",
    )

    bot = Bot(
        output_device_index=config["SPEECH_RECOGNITION"].getint(
            "OUTPUT_DEVICE_INDEX", fallback=None
        ),
        input_device_index=config["SPEECH_RECOGNITION"].getint(
            "INPUT_DEVICE_INDEX", fallback=None
        ),
        adjust_for_ambient_noise=config["SPEECH_RECOGNITION"].getboolean(
            "ADJUST_FOR_AMBIENT_NOISE", fallback=False
        ),
        language=config["SPEECH_RECOGNITION"].get("LANGUAGE", fallback="en-US"),
        wit_access_token=config["WIT.AI"].get("ACCESS_TOKEN"),
        confidence_treshold=config["WIT.AI"].getfloat(
            "CONFIDENCE_TRESHOLD", fallback=0.90
        ),
        names=config["SPEECH_RECOGNITION"].get("NAMES", "user,username"),
    )
    if config["OTHER"].getboolean("NEVER_PREPROCESS_FILES") == False:
        bot.preprocess_files(
            keep_files=config["OTHER"].getboolean("KEEP_PROCESSED_FILES", fallback=True)
        )
    bot.start()

    # never ending loop so our bot keeps running
    while True:
        time.sleep(0.5)
