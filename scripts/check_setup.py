"""Quick health check: run with  uv run python scripts/check_setup.py"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ok = True


def report(name, passed, detail=""):
    global ok
    ok = ok and passed
    print(f"[{'ok' if passed else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


# 1. Python packages
for pkg in ["numpy", "pandas", "sklearn", "networkx", "matplotlib", "neo4j", "chromadb", "groq", "dotenv", "ipykernel"]:
    try:
        __import__(pkg)
        report(f"import {pkg}", True)
    except ImportError:
        report(f"import {pkg}", False, "run: uv sync")

# 2. .env and Neo4j
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")
uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD")
if not (ROOT / ".env").exists():
    report(".env file", False, "copy .env.example to .env and set NEO4J_PASSWORD")
elif not password or password == "change_me":
    report("NEO4J_PASSWORD", False, "set your real password in .env")
else:
    try:
        from neo4j import GraphDatabase

        with GraphDatabase.driver(uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            with driver.session() as session:
                value = session.run("RETURN 1 AS x").single()["x"]
        report("Neo4j connection", value == 1, uri)
    except Exception as e:  # noqa: BLE001
        if type(e).__name__ == "AuthError":
            report("Neo4j connection", False, "Neo4j is running but the password in .env is wrong")
        else:
            report("Neo4j connection", False, f"{type(e).__name__}: {str(e)[:100]}  (is Neo4j running?)")

# Groq key (the notebook runs without it, but the written case summary needs it)
if os.environ.get("GROQ_API_KEY"):
    report("GROQ_API_KEY", True, "found")
else:
    print("[note] GROQ_API_KEY not set: the written case summary will show a fallback message (see docs/env-and-groq.md)")

# 3. ChromaDB can write and read from disk (uses its own scratch folder under data/)
try:
    import traceback

    import chromadb

    client = chromadb.PersistentClient(path=str(ROOT / "data" / "_check_chroma"))
    try:
        client.delete_collection("check")
    except Exception:  # noqa: BLE001
        pass
    col = client.create_collection("check", metadata={"hnsw:space": "cosine"})
    col.add(ids=["a", "b"], embeddings=[[1.0, 0.0], [0.0, 1.0]], documents=["x", "y"])
    best = col.query(query_embeddings=[[1.0, 0.1]], n_results=1)["ids"][0][0]
    report("ChromaDB write and query", best == "a")
except Exception as e:  # noqa: BLE001
    traceback.print_exc()
    report("ChromaDB write and query", False, f"{type(e).__name__}")

print("\nAll checks passed." if ok else "\nSome checks failed. Neo4j is optional: the notebook still runs without it.")
sys.exit(0 if ok else 1)
