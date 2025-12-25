import time
from datetime import datetime
from engine import run
from telegram import send

# 🚀 STARTUP MESSAGE
send("🚀 Trading Bot STARTED & RUNNING")

while True:
    run()

    now = datetime.utcnow()

    # 💓 HEARTBEAT tiap jam (menit 00)
    if now.minute == 0:
        send("💓 Engine still running")

    time.sleep(60)
