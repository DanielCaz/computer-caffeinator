import os
import pyautogui as pt
from settings import config


def main():
    ms_word_path = config["ms_word_path"]

    if not os.path.exists(ms_word_path):
        print(f"Error: MS Word executable not found at {ms_word_path}")
        return

    os.startfile(ms_word_path)

    pt.sleep(config["delays"]["app_start"])  # Wait for MS Word to open

    coords = config["coordinates"]["blank_document"]
    pt.moveTo(  # Coordinates for 'Blank document' (may vary by screen resolution)
        coords["x"],
        coords["y"],
        duration=1,
    )
    pt.click()

    pt.sleep(config["delays"]["doc_ready"])  # Wait for the new document to be ready

    text = config["automation"]["text"]
    interval = config["automation"]["interval"]

    for _ in range(config["automation"]["loop_count"]):
        pt.typewrite(text, interval=interval)

        pt.sleep(config["delays"]["line_pause"])  # Pause between lines


if __name__ == "__main__":
    main()
