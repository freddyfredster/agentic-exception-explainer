import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4.1-mini"  # or similar small, cheap model

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
KPI_DIR = os.path.join(DATA_DIR, "kpi")
KPI_FILE = os.path.join(KPI_DIR, "KPI_Facts.csv")
VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")
