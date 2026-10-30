import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DATABASE_URL","sqlite+aiosqlite:///./test.db")
os.environ.setdefault("LLM_PROVIDER","ollama")
