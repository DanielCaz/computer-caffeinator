# Computer Caffeinator

A Python automation script that keeps your computer active by simulating user activity in Microsoft Word. It opens Word, creates a new document, and types text repeatedly.

## Why the name?

Because it stops your computer from going to sleep and keeps it "caffeinated".

## Features

- Automates Microsoft Word startup and interaction
- Configurable settings via `config.json`
- Simulates mouse movement and keyboard typing
- Customizable typing speed and loop count

## Requirements

- Python 3.12 or higher
- [pyautogui](https://pypi.org/project/PyAutoGUI/)
- Microsoft Word (installed at the configured path)

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

## Configuration

The project uses a `config.json` file to manage settings. You can customize the following:

- `ms_word_path`: Path to the Microsoft Word executable.
- `coordinates`: Screen coordinates for clicking the "Blank document" template.
- `automation`: Text to type, typing interval, and loop count.
- `delays`: Wait times for application startup and document loading.

Example `config.json`:

```json
{
  "ms_word_path": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
  "coordinates": {
    "blank_document": {
      "x": 300,
      "y": 250
    }
  },
  "automation": {
    "text": "This is an automated line typed by PyAutoGUI.\n",
    "interval": 0.05,
    "loop_count": 5
  },
  "delays": {
    "app_start": 5,
    "doc_ready": 3,
    "line_pause": 1
  }
}
```

## Usage

Run the application with:

```sh
uv run main.py
```

The script will:

1. Launch Microsoft Word.
2. Click at the configured coordinates (default is for "Blank document").
3. Type the configured text repeatedly into the document.

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
