# SearchIt 🔍

Making a lost and found item web application for college campus.

## 🚀 Running SearchIt Locally

You can run SearchIt locally without opening an IDE in a few easy ways:

### Option 1: Double-Click (Windows)
Double-click `run.bat` in the project root directory.
- Automatically activates your `.venv` virtual environment if present.
- Launches the Flask server at `http://127.0.0.1:5000`.
- Automatically opens your default web browser to `http://127.0.0.1:5000`.

### Option 2: Terminal / Command Line
Run the following command from the project root:

```bash
python run.py
```

Or using Flask directly:

```bash
python app.py
```

### Setup & Requirements
If running for the first time:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
