import sqlite3
import secrets
import time
import hashlib

DB = "keys.db"

def connect():
    return sqlite3.connect(DB)

def setup():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key_hash TEXT PRIMARY KEY,
                discord_id TEXT NOT NULL,
                expires_at INTEGER NOT NULL
            )
        """)

def generate_key(discord_id):
    key = secrets.token_urlsafe(18)
    key_hash = hashlib.sha256(key.encode()).hexdigest()

    with connect() as db:
        db.execute(
            "DELETE FROM keys WHERE discord_id = ?",
            (str(discord_id),)
        )
        db.execute(
            "INSERT INTO keys VALUES (?, ?, ?)",
            (key_hash, str(discord_id), int(time.time()) + 86400)
        )

    return key

def verify_key(key, discord_id):
    key_hash = hashlib.sha256(key.encode()).hexdigest()

    with connect() as db:
        result = db.execute(
            "SELECT discord_id, expires_at FROM keys WHERE key_hash = ?",
            (key_hash,)
        ).fetchone()

    if not result:
        return False

    owner, expiry = result
    return owner == str(discord_id) and time.time() < expiry
