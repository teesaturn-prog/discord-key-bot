import os
import threading
import logging

import bot
from api import app
from waitress import serve

logging.basicConfig(level=logging.INFO)

def run_bot():
    try:
        logging.info("Starting Discord bot...")
        bot.bot.run(os.environ["DISCORD_TOKEN"])
    except Exception:
        logging.exception("Discord bot crashed")

if __name__ == "__main__":
    threading.Thread(
        target=run_bot,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 10000))

    logging.info(f"Starting API server on port {port}")

    serve(
        app,
        host="0.0.0.0",
        port=port
    )
