# 3. The `.env` file: Neo4j password and Groq key

The notebook reads its secrets from a file named `.env` in the project's main folder, next to `pyproject.toml`. **Never commit this file.** `.gitignore` already excludes it.

## Create it
In PowerShell, from the project folder:

```
copy .env.example .env
code .env
```

On macOS or Linux, use `cp .env.example .env` instead of `copy`.

If `code` is not recognized, open the folder in VS Code and click `.env` in the sidebar.

## What goes in it

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
GROQ_API_KEY=your_groq_key
```

No spaces around `=`, and no quotes. The file must be named `.env`, not `.env.txt`. Windows hides file extensions by default, so check with `dir -Force`.

## The Neo4j password
This is the password you chose when you first logged in to http://localhost:7474/browser/. See [neo4j-windows-setup.md](neo4j-windows-setup.md) (or [neo4j-mac-linux-setup.md](neo4j-mac-linux-setup.md)) for how to set, change or recover it. Keep `NEO4J_URI` as it is unless you changed Neo4j's port.

## The Groq key
Groq hosts the language model that writes the case summary at the end of the notebook. Create an API key in your Groq account (https://console.groq.com/keys) and paste it after `GROQ_API_KEY=`.

- The `groq` package is installed by `uv sync`, so you do not install anything extra.
- The notebook uses the model `openai/gpt-oss-120b`. If Groq retires or renames that model, change the `MODEL` line in the notebook.
- The model is told to use only the facts in the case file, and to never describe a rung 1 finding as a cause.
- The key is optional in the sense that the notebook still runs without it, and the written summary shows a fallback message. For the full demo, add it.

## Check it
```
uv run python scripts/check_setup.py
```

You want `[ok] Neo4j connection` and `[ok] GROQ_API_KEY`. The check confirms the key is present, but it does not call Groq. The first real test is the last cells of the notebook.
