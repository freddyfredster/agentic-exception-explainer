from typing import List, Dict, Any

import pandas as pd
import chromadb
from chromadb.config import Settings

from .config import KPI_FILE, VECTORSTORE_DIR

# ---------------------------------------
# KPI QUERY TOOL
# ---------------------------------------

_kpi_df_cache = None

def _load_kpi_df() -> pd.DataFrame:
    global _kpi_df_cache
    if _kpi_df_cache is None:
        _kpi_df_cache = pd.read_csv(KPI_FILE)
    return _kpi_df_cache

def query_kpi(yearmonth: str, product: str, region: str) -> Dict[str, Any]:
    df = _load_kpi_df()

    subset = df[
        (df["YearMonth"] == yearmonth) &
        (df["Product"] == product) &
        (df["Region"] == region)
    ]

    if subset.empty:
        return {
            "found": False,
            "message": "No data found for that YearMonth/Product/Region combination."
        }

    row = subset.iloc[0]  # only one row per combination in our dummy dataset

    sales = float(row["Sales"])
    last = None if pd.isna(row["Sales_LastMonth"]) else float(row["Sales_LastMonth"])
    change_pct = None

    if last and last > 0:
        change_pct = (sales - last) / last * 100.0

    return {
        "found": True,
        "yearmonth": yearmonth,
        "product": product,
        "region": region,
        "sales": sales,
        "sales_last_month": last,
        "change_vs_last_month_pct": change_pct,
        "raw_row": row.to_dict()
    }

QUERY_KPI_TOOL = {
    "type": "function",
    "function": {
        "name": "query_kpi",
        "description": "Retrieve KPI data for a given month, product, and region.",
        "parameters": {
            "type": "object",
            "properties": {
                "yearmonth": {"type": "string"},
                "product": {"type": "string"},
                "region": {"type": "string"}
            },
            "required": ["yearmonth", "product", "region"]
        }
    }
}

# ---------------------------------------
# DOC SEARCH TOOL
# ---------------------------------------

def _get_chroma_collection():
    client = chromadb.PersistentClient(
        path=VECTORSTORE_DIR,
        settings=Settings()
    )
    return client.get_collection("docs")

def search_docs(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    collection = _get_chroma_collection()

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    output = []
    for doc, meta, id_ in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["ids"][0]
    ):
        output.append({
            "id": id_,
            "text": doc,
            "file_id": meta.get("file_id"),
            "source_type": meta.get("source_type")
        })

    return output

SEARCH_DOCS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": "Search notes/emails for text relevant to KPI explanations.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}
