import sqlite3
from pathlib import Path
from datetime import datetime, timezone
<<<<<<< HEAD
from app.config import settings

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class OutreachDB:
    def __init__(self, path=None):
        if path is None:
            if not settings.database_url.startswith("sqlite:///"):
                raise ValueError("Only sqlite DATABASE_URL values are supported")
            path = settings.database_url.removeprefix("sqlite:///")
        path = Path(path)
        if not path.is_absolute():
            path = ROOT_DIR / path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path = str(path)
=======

class OutreachDB:
    def __init__(self, path="data/outreach.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path = path
>>>>>>> origin/main
        with sqlite3.connect(path) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS outreach(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                influencer TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
                message_generated TEXT NOT NULL, sent INTEGER NOT NULL DEFAULT 0,
                sent_at TEXT, status TEXT NOT NULL, provider_message_id TEXT)""")

    def already_sent(self, email):
        with sqlite3.connect(self.path) as c:
            return c.execute("SELECT 1 FROM outreach WHERE email=? AND status IN ('sent','simulated')",
                             (email,)).fetchone() is not None

    def record(self, influencer, email, message, status, provider_message_id):
        sent = int(status in {"sent","simulated"})
        when = datetime.now(timezone.utc).isoformat() if sent else None
        with sqlite3.connect(self.path) as c:
            c.execute("""INSERT OR IGNORE INTO outreach
                (influencer,email,message_generated,sent,sent_at,status,provider_message_id)
                VALUES(?,?,?,?,?,?,?)""",
                (influencer,email,message,sent,when,status,provider_message_id))
<<<<<<< HEAD

    def records(self):
        with sqlite3.connect(self.path) as c:
            c.row_factory = sqlite3.Row
            return [dict(row) for row in c.execute("""
                SELECT influencer, email, message_generated, sent, sent_at, status,
                       provider_message_id
                FROM outreach ORDER BY id DESC
            """)]
=======
>>>>>>> origin/main
