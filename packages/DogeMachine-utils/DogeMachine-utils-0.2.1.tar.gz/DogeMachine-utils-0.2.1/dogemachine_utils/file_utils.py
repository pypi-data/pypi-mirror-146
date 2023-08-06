import os
import logging
import csv
import json
import yaml
logger = logging.getLogger(__name__)


def write_file(file: str, content: str) -> None:
    if os.path.exists(file):
        logger.debug("%s exists. Removing the file and replacing its contents." % file)
        os.remove(file)
    with open(file, "w") as f:
        f.write(content)


def read_file(file: str) -> str:
    with open(file, "r") as f:
        content = f.read()
    return content


def create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def read_yaml_file(filename: str) -> dict:
    with open(filename, "r") as yaml_file:
        cfg = yaml.safe_load(yaml_file)
    return cfg


def read_json_file(file: str) -> dict:
    with open(file) as f:
        contents = f.read()
        try:
            results = json.loads(contents)
        except json.decoder.JSONDecodeError as error:
            logger.debug(error)
            decoded_data = contents.encode().decode("utf-8-sig")
            results = json.loads(decoded_data)
    return results
