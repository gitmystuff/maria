# 1. Python environment (uv)

The project uses [uv](https://docs.astral.sh/uv/) to create the environment and install every package from `pyproject.toml`. Nothing needs to be installed one package at a time.

## Install uv
If `uv --version` already works in your terminal, skip this step. Otherwise install it, then open a new terminal.

- **Windows (PowerShell):**

  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- **macOS or Linux:**

  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

These are the commands from uv's own installation page, which has other options (Homebrew, WinGet, pip): https://docs.astral.sh/uv/getting-started/installation/ . Check that page if a command has changed.

## Install everything
From the project folder (the one that contains `pyproject.toml`):

```
uv sync
```

This creates a `.venv` folder and installs all of these:

| Package | Used for |
|---|---|
| numpy, pandas, scikit-learn | Data, the fraud model, and the TF-IDF check |
| networkx, matplotlib | The graph and the plots |
| neo4j | The Neo4j driver |
| chromadb | The persistent vector store |
| groq | The client for the written case summary |
| python-dotenv | Reads your `.env` file |
| ipykernel, jupyterlab | Runs the notebook |

uv also installs the Python version the project asks for (see `.python-version`) if it is not already on your computer.

## Check it
```
uv run python scripts/check_setup.py
```

The lines that start with `import` should all show `[ok]`. The Neo4j and Groq lines need the next two guides first.

## Adding or updating a package later
```
uv add package_name
```

This updates `pyproject.toml` and `uv.lock`. Commit both to GitHub.
