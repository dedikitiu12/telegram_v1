port time
import schedule
from utils.notifier import send_telegram_message
from utils.indicators import analyze_indicators
from utils.price_action import detect_price_action
from utils.ob_fvg_logic import detect_ob_fvg_signal
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, GOLD_API_KEY
import requests

# Fungsi untuk ambil data harga XAUUSD dari GoldAPI
def fetch_gold_data():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": GOLD_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return {
            "price": data.get("price"),
            "open": data.get("open_price"),
            "high": data.get("high_price"),
            "low": data.get("low_price"),
            "timestamp": data.get("timestamp")
        }
    except Exception as e:
        print(f"[ERROR] Gagal fetch data GoldAPI: {e}")
        return None

# Fungsi utama analisa & kirim sinyal
def run_signal_bot():
    print("⏳ Mengambil data XAUUSD...")
    gold_data = fetch_gold_data()

    if not gold_data:
        print("❌ Data tidak tersedia. Bot dihentikan sementara.")
        return

    print(f"✅ Data diterima: {gold_data}")

    # 1. Analisa indikator teknikal
    indicator_signal = analyze_indicators(gold_data)

    # 2. Deteksi pola candlestick / price action
    price_action_signal = detect_price_action(gold_data)

    # 3. Deteksi sinyal OB/FVG/BOS
    ob_fvg_signal, signal_rating = detect_ob_fvg_signal(gold_data)

    # Gabungkan semua hasil analisa
    final_message = f"""
📡 *Sinyal XAUUSD Terdeteksi!*

💰 Harga Saat Ini: ${gold_data['price']}
🕒 Timestamp: {gold_data['timestamp']}

📊 *Indikator*:
{indicator_signal}

🕯️ *Price Action*:
{price_action_signal}

🧠 *Order Block/FVG/BOS*:
{ob_fvg_signal}

⭐ *Rating Sinyal*: {signal_rating}/5

📝 *Saran*: Lakukan konfirmasi tambahan sebelum entry.
    """.strip()

    # Kirim ke Telegram
    send_telegram_message(final_message)

# Jadwalkan setiap 30 menit Senin–Jumat
schedule.every(30).minutes.do(run_signal_bot)

print("✅ Bot sinyal XAUUSD aktif dan berjalan...")

# Looping terus
while True:
    schedule.run_pending()
    time.sleep(1)
