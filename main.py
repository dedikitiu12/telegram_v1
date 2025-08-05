import time
import schedule
from utils.ob_fvg_logic import analyze_market
from utils.notifier import send_telegram_message
from config import SYMBOL, INTERVAL, GOLDAPI_KEY

def run_bot():
    try:
        print("⏳ Memulai analisa market...")
        signal = analyze_market(SYMBOL, INTERVAL, GOLDAPI_KEY)
        if signal:
            send_telegram_message(signal)
        else:
            print("❌ Tidak ada sinyal valid.")
    except Exception as e:
        print(f"❗ Error saat menjalankan bot: {e}")

# Atur agar dijalankan setiap 1 jam (Senin–Jumat)
schedule.every(1).hours.do(run_bot)

print("🤖 Bot sinyal XAUUSD aktif...")

while True:
    schedule.run_pending()
    time.sleep(10)

