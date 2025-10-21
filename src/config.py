# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
DOWNLOADS_DIR = ROOT_DIR / "downloads"
NOTES_DIR = ROOT_DIR / "notes"
