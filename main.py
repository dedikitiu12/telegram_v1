import time
import datetime
import requests
from utils.indicators import calculate_indicators
from utils.price_action import check_price_action
from utils.ob_fvg_logic import analyze_ob_fvg
from utils.notifier import send_telegram_message
from config import GOLDAPI_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Parameter default
PAIR = "XAUUSD"
GOLDAPI_URL = f"https://www.goldapi.io/api/{PAIR}"

HEADERS = {
    "x-access-token": GOLDAPI_KEY,
    "Content-Type": "application/json"
}

def get_gold_price():
    try:
        response = requests.get(GOLDAPI_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return {
                "price": data.get("price"),
                "ask": data.get("ask"),
                "bid": data.get("bid"),
                "timestamp": data.get("timestamp")
            }
        else:
            print(f"[ERROR] Gagal ambil data GoldAPI: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception saat ambil data: {e}")
        return None

def analyze_market():
    market_data = get_gold_price()
    if not market_data:
        return

    price = market_data["price"]
    timestamp = datetime.datetime.fromtimestamp(market_data["timestamp"])

    print(f"\n[{timestamp}] Harga XAUUSD: {price}")

    # Indikator teknikal
    indicators = calculate_indicators(price)
    
    # Price action: Doji, Engulfing, Pinbar, dst
    price_signal = check_price_action(price)
    
    # OB, FVG, BOS, Liquidity Sweep
    ob_fvg_signal, rating = analyze_ob_fvg(price)

    # Gabungkan sinyal
    if price_signal or ob_fvg_signal:
        message = f"📢 *Sinyal Trading XAUUSD Detected!*\n\n"
        message += f"💰 *Harga Sekarang:* {price}\n"
        message += f"📈 *Timestamp:* {timestamp}\n\n"

        if indicators:
            message += f"📊 *Indikator:*\n{indicators}\n"
        if price_signal:
            message += f"🕯️ *Price Action:* {price_signal}\n"
        if ob_fvg_signal:
            message += f"🧠 *Smart Money Concepts:* {ob_fvg_signal}\n"
            message += f"⭐ *Rating Sinyal:* {rating} / 5\n"

        message += "\n🚀 *Sinyal Otomatis oleh Bot AI*"
        send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)
    else:
        print("📭 Tidak ada sinyal hari ini.")

def is_weekday():
    hari = datetime.datetime.now().weekday()
    return hari < 5  # 0 = Senin, 4 = Jumat

if __name__ == "__main__":
    print("🚀 Bot Sinyal XAUUSD Aktif...")
    while True:
        if is_weekday():
            analyze_market()
        else:
            print("📅 Akhir pekan, bot istirahat...")

        time.sleep(60 * 30)  # Cek setiap 30 menit
