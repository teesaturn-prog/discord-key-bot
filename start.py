
import os
import threading
import bot
from api import app

def run_bot():
    bot.bot.run(os.environ["DISCORD_TOKEN"])

threading.Thread(
    target=run_bot,
    daemon=True
).start()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0",
          port=int(os.environ.get("PORT", 10000)))
