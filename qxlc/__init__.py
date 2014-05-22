#!/usr/bin/env python3
#
# Copyright 2014 Dabo Ross <http://www.daboross.net/>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import logging.config
import os
import sys

from flask import Flask

from pushbullet import PushBullet

__all__ = ["app", "config", "push", "device"]

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "brief": {
            "format": "[%(asctime)s][%(levelname)s] %(message)s",
            "datefmt": "%H:%M:%S"
        },
        "full": {
            "format": "[%(asctime)s][%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d][%H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "brief",
            "level": "WARNING",
            "stream": "ext://sys.stderr"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "full",
            "level": "DEBUG",
            "filename": "qxlc.log"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
})


def get_config():
    config_path = os.path.abspath("config.json")
    if os.path.isfile(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)
    else:
        logging.warning("Config not found! Please copy config.default.json to config.json")
        sys.exit()


config = get_config()

app = Flask(__name__)

_api_key = config["pushbullet"]["api-key"]
device = config["pushbullet"]["device"]
push = PushBullet(_api_key)

from qxlc import minifier, error_handlers
