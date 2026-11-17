# Troubleshooting

Start with `uv run python scripts/check_setup.py`. It tells you which piece is failing.

## Neo4j

| What you see | What it means | What to do |
|---|---|---|
| `AuthError` or "unauthorized" | Neo4j is running, but the password in `.env` is wrong | Fix `NEO4J_PASSWORD`. To change or recover the password, see [neo4j-windows-setup.md](neo4j-windows-setup.md) |
| "Could not connect" or `ServiceUnavailable` | Neo4j is not running, or the port is wrong | Make sure the `neo4j console` window is still open. Check `NEO4J_URI` |
| "No NEO4J_PASSWORD found" | `.env` is missing, misnamed, or in the wrong folder | Put `.env` next to `pyproject.toml`. Check it is not `.env.txt` (`dir -Force`) |
| PowerShell: "The module '%NEO4J_HOME%' could not be loaded" | `%NEO4J_HOME%` is Command Prompt syntax | In PowerShell use `& "$env:NEO4J_HOME\bin\neo4j" console` |
| `echo $env:NEO4J_HOME` prints nothing | The variable is not set in this window | Open a new terminal. If still empty, rerun `setx NEO4J_HOME "C:\neo4j-community-2026.09.0"` |
| Neo4j will not start | Often Java | `java -version` should show 21 |
| Port 7474 or 7687 already in use | Another Neo4j is running | Stop it, then start again |

## Groq
| What you see | What to do |
|---|---|
| `[OFFLINE FALLBACK -- no GROQ_API_KEY found...]` | Add `GROQ_API_KEY=...` to `.env`, then **restart the notebook kernel** so it rereads the file |
| `No module named 'groq'` | Run `uv sync`, and make sure the notebook uses the project's `.venv` kernel |
| `[Groq API error: ...]` with a message about the model | The model name may have changed. Update the `MODEL` line in the notebook |
| `[Groq API error: ...]` about the key or authorization | The key is wrong or revoked. Create a new one |

## ChromaDB
| What you see | What to do |
|---|---|
| Errors after a package upgrade | Delete the folder `data\chroma` and rerun the notebook. It rebuilds the collection |
| "file is being used by another process" on Windows | Close other notebooks or terminals using the project, then retry |

## Python and VS Code
| What you see | What to do |
|---|---|
| `ModuleNotFoundError` in the notebook | You selected the wrong kernel. Choose the `.venv` inside this project folder, or run `uv sync` again |
| VS Code does not list the `.venv` | Run `uv sync` first, then reload the VS Code window (Ctrl+Shift+P, then "Reload Window") |
| Changes to `.env` are ignored | The notebook read `.env` when the kernel started. Restart the kernel |
