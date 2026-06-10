# Agentic AI Crash Course

A small collection of example code and notebooks in my journey of learning Generative AI and Agentic AI

## Contents

- `main.py` — project entry point / example runner
- `01_llm_call/call_llm.ipynb` — Jupyter notebook with LLM examples
- `pyproject.toml` — project metadata and dependencies

## Requirements

- Python 3.14 or newer
- Recommended: a virtual environment (venv, virtualenv, or Poetry)

## Setup

Using Poetry (recommended if installed):

```
poetry install
```

If you prefer pip, export a `requirements.txt` from Poetry then install:

```
poetry export -f requirements.txt --without-hashes -o requirements.txt
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# or .venv\Scripts\activate.bat   # cmd.exe
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you don't use Poetry, you can manually create a venv and install the dependencies listed in `pyproject.toml`.

## Quick Start

Run the example script:

```
python main.py
```

Open and run the notebook:

```
jupyter notebook 01_llm_call/call_llm.ipynb
```

## Notes

- Dependencies are declared in `pyproject.toml`. See that file for exact package versions.
- This repo is intended for learning and experimentation; not production-ready.

