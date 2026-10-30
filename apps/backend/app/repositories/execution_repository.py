# Repository layer: persistence is best-effort so in-memory execution still succeeds when DB is down.
# See services/chat_service.py for the write path; reads fall back to the in-memory store.
