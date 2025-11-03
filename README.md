# Computer Caffeinator

A simple Tkinter-based desktop app that simulates typing in a text entry box. The app can repeatedly type out "hello world" in a typewriter effect, with Start and Stop buttons to control the animation.

## Why the name?

Because it stops your computer from going to sleep and keeps it "caffeinated".

## Features

- Minimal GUI using Tkinter
- Typewriter animation effect for text
- Start and Stop controls
- Easy to run, no external dependencies except Tkinter (standard library) and pyautogui (for future enhancements)

## Requirements

- Python 3.12 or higher
- [pyautogui](https://pypi.org/project/PyAutoGUI/) (installed automatically if using `pyproject.toml`)

## Installation

1. Clone this repository or download the source code.
2. (Recommended) Create a virtual environment:
   ```sh
   uv venv
   ```
3. Install dependencies:
   ```sh
   uv sync
   ```

## Usage

Run the application with:

```sh
uv run main.py
```

This will open a window with a text entry and Start/Stop buttons. Clicking Start will animate typing "hello world" in the entry box. Stop will halt the animation.

## Development

For code formatting, linting, and type checking, use the following tools (already listed in the `pyproject.toml`):

- [black](https://black.readthedocs.io/en/stable/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [mypy](http://mypy-lang.org/)

## Building from Source

Use pyinstaller to create an executable:

```sh
uvx pyinstaller --onefile main.py
```

## License

MIT License
