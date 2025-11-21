import json
import os
import sys


# Get the directory where the executable/script is located
if getattr(sys, "frozen", False):
    # Running as a PyInstaller executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "ms_word_path": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "coordinates": {"blank_document": {"x": 300, "y": 250}},
    "automation": {
        "text": "This is an automated line typed by PyAutoGUI.",
        "interval": 0.5,
        "loop_count": 10,
    },
    "delays": {"app_start": 5, "doc_ready": 3, "line_pause": 1},
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


config = load_config()
