# 4. Run the notebook in VS Code

## Before you start
All of these should be done:
1. `uv sync` finished ([python-environment.md](python-environment.md))
2. Neo4j is running in its own window ([neo4j-windows-setup.md](neo4j-windows-setup.md))
3. `.env` has your Neo4j password and Groq key ([env-and-groq.md](env-and-groq.md))
4. `uv run python scripts/check_setup.py` shows `[ok]` on every line

## Open and run
1. Open the project folder in VS Code (**File > Open Folder**).
2. Install the **Python** and **Jupyter** extensions if VS Code asks.
3. Open `notebooks/case_file_crm_story.ipynb` (the story edition; `case_file_crm.ipynb` is the shorter original).
4. Click **Select Kernel** at the top right, then **Python Environments**, and choose the `.venv` inside this project folder. The environment must be the one `uv sync` created, or the packages will not be found.
5. Click **Run All**. A full run takes under a minute.

## What to check as it runs
- The first code cells should print `Connected to Neo4j at bolt://localhost:7687`. If they print "No NEO4J_PASSWORD" or "Could not connect", fix that first (see [troubleshooting.md](troubleshooting.md)).
- Part 3 stores the note vectors in ChromaDB and prints that the collection is still there after reopening.
- Part 5 builds the Neo4j graph, loads the customers and interactions, and runs the Cypher queries, including the customer 360 for Maria.
- The last section prints the case file and then the written summary. If you see "[Groq API error...]", see [troubleshooting.md](troubleshooting.md).

## Running it again
The notebook is safe to rerun. It deletes and rebuilds every Neo4j node carrying its own labels (Claim, Shop, Area, Adjuster, Customer, Interaction), its own ChromaDB collection (`claim_notes`) and, in the story edition, its own SQLite tables. Your other Neo4j data is left alone.

## Alternative: JupyterLab
```
uv run jupyter lab
```

then open `notebooks/case_file_crm.ipynb` in the browser.
