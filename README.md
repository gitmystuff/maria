# From Look-Alikes to Action: A Case File for Maria

A teaching notebook for a data analysis and knowledge discovery course. One running fraud-insurance story (Maria, an honest claimant flagged by a model) ties together:

- **Similarity retrieval** with a hand-built TF-IDF, and a persistent **ChromaDB** vector store
- **Clustering** with a hand-built k-means, read as customer segments
- A **knowledge graph** in NetworkX and **Neo4j** (Cypher), including customers and an interaction log
- **CRM**: customer record, customer 360, retention, a business case, and a randomized pilot
- **Causal validation** on Pearl's ladder: seeing, doing and imagining
- A grounded **case file**, summarized by a language model through **Groq**

Everything is simulated, with planted truth, so each answer can be checked.

## What you need installed

**This demo is built to run with everything below installed.** Set up all four items before you open the notebook.

| # | What | Why it is needed | Guide |
|---|---|---|---|
| 1 | **Python environment** (uv) with all packages, including ChromaDB, the Neo4j driver, the Groq client and Jupyter. The guide shows how to install uv itself. | Runs the notebook | [docs/python-environment.md](docs/python-environment.md) |
| 2 | **Neo4j Community**, running on your computer | The knowledge graph and customer 360 | [Windows](docs/neo4j-windows-setup.md) or [macOS and Linux](docs/neo4j-mac-linux-setup.md) |
| 3 | **A `.env` file** with your Neo4j password and a Groq API key | Connects the notebook to Neo4j and to the language model | [docs/env-and-groq.md](docs/env-and-groq.md) |
| 4 | **VS Code** with the Python and Jupyter extensions | Where the notebook is run | [docs/run-the-notebook.md](docs/run-the-notebook.md) |

ChromaDB needs no separate install. It is a Python package that stores its data in a folder inside the project.

If something is missing, the notebook degrades instead of stopping: without Neo4j the Neo4j cells are skipped, and without a Groq key the written summary shows a fallback message. But the demo is meant to be shown with all of it working.

## Quick start

From the project folder. In PowerShell on Windows:

```
uv sync
copy .env.example .env
```

On macOS or Linux, in a terminal:

```
uv sync
cp .env.example .env
```

Edit `.env` (see [docs/env-and-groq.md](docs/env-and-groq.md)), start Neo4j (see [Windows](docs/neo4j-windows-setup.md) or [macOS and Linux](docs/neo4j-mac-linux-setup.md)), then verify everything:

```
uv run python scripts/check_setup.py
```

When every line shows `[ok]`, open a notebook from `notebooks/` in VS Code (`case_file_crm_story.ipynb` is the narrated story edition; `case_file_crm.ipynb` is the shorter original) ([docs/run-the-notebook.md](docs/run-the-notebook.md)). If anything fails, see [docs/troubleshooting.md](docs/troubleshooting.md).

## The notebooks

**`case_file_crm_story.ipynb`, the story edition.** One customer, Maria, is flagged by a fraud model although her claim is legitimate. Each part answers a question she would ask, and every part has the same layers:

- **Narrate** boxes: the story in plain words, written to be read aloud.
- **Concept** boxes: the idea in a sentence or two.
- **Dig deeper** sections: the details, formulas and code explained, for anyone who wants to go further.
- **Go further on your own**: documentation links, something to try and a question to think about.

| Part | Maria's question | Tools |
|---|---|---|
| 1 | Why was I flagged? | Logistic regression (scikit-learn) |
| 2 | What is in the files about me? | pandas tables, the customer (CRM) layer |
| 3 | Who else looks like me? | Hand-built TF-IDF and cosine similarity, ChromaDB |
| 4 | Which group am I in? | Hand-built k-means, customer segments |
| 5 | How am I connected? | NetworkX, Neo4j and Cypher, customer 360 |
| 6 | Which store answers which question? | SQLite (SQL), Cypher, vector search side by side |
| 7 | Is my repair shop to blame? | Causal diagram, adjustment, do() |
| 8 | Did the false alarm cost the insurer my business? | Adjustment, counting lapses, sensitivity |
| 9 | What would reviewing more claims be worth? | A business case with labeled assumptions |
| 10 | What would have happened to me, and what do I need now? | Counterfactuals for one person |
| 11 | Does the fix work? | A randomized pilot, ranges, sample size |
| 12 | What goes in my file? | A grounded case file, optional language-model summary (Groq) |
| 13 | What should worry us? | Limits, privacy and fairness |

**`case_file_crm.ipynb`** is the shorter original without the narration and the SQLite part.

The notebooks do not need a GPU.

## Layout

```
.
├── notebooks/case_file_crm_story.ipynb  the story edition: Maria's story with narration, concepts and all three databases
├── notebooks/case_file_crm.ipynb      the shorter original notebook
├── scripts/check_setup.py             health check for packages, Neo4j, ChromaDB and the Groq key
├── docs/
│   ├── python-environment.md          install uv and the packages
│   ├── neo4j-windows-setup.md         install and start Neo4j on Windows
│   ├── neo4j-mac-linux-setup.md       install and start Neo4j on macOS and Linux (untested)
│   ├── env-and-groq.md                the .env file, Neo4j password, Groq key
│   ├── run-the-notebook.md            open and run the notebook in VS Code
│   └── troubleshooting.md             common errors and fixes
├── data/                              ChromaDB and SQLite files are written here (not committed)
├── pyproject.toml, uv.lock            dependencies, managed with uv
├── .env.example                       copy to .env (never commit .env)
├── LICENSE                            MIT, for the code
├── LICENSE-CONTENT.md                 CC BY 4.0, for the written material
└── .gitignore
```

## What gets stored where

| Store | What it holds | Where | Rebuilt by |
|---|---|---|---|
| ChromaDB | TF-IDF vectors of the 6,000 adjuster notes, with the note text and metadata | `data/chroma/` | The notebook (it deletes and recreates its own collection, `claim_notes`) |
| Neo4j | Claims, shops, areas, adjusters, customers and interactions | Your local Neo4j database | The notebook (it deletes every node that carries one of its labels, so use a database that does not use those labels for other data) |
| SQLite | The claims, customers and interactions tables (story edition only) | `data/claims_crm.sqlite` | The story notebook (it replaces its own three tables) |

All three are safe to delete and regenerate. The random seeds are fixed, so a rerun reproduces the same numbers.

## Not using Windows?

The commands above that use `copy` become `cp` on macOS and Linux, and Neo4j has its own guide ([docs/neo4j-mac-linux-setup.md](docs/neo4j-mac-linux-setup.md)). That guide has not been tested on those systems for this project. Everything else (uv, ChromaDB, SQLite, the notebooks) is plain Python and should work the same way on any system, though it has so far been run only on Windows and Linux.

## License

- **Code** (the Python files and the code cells in the notebooks): [MIT License](LICENSE).
- **Written material** (the narration and explanations in the notebooks, the guides in `docs/`, and this README): [CC BY 4.0](LICENSE-CONTENT.md). You may reuse and adapt it, with credit.

The packages this project installs (NumPy, pandas, ChromaDB, Neo4j driver and the rest) keep their own licenses. Neo4j itself is installed separately and is not part of this repository.

## Notes for students and reviewers

- All dollar figures in the business-case section are illustrative assumptions.
- Customer records are personal data in real life. The notebook ends with a discussion of privacy and fairness.
- Never commit `.env`. It holds your passwords and API key, and `.gitignore` already excludes it.
