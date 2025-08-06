import requests
import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def format_signal_message(signal_data):
    """
    Format isi pesan sinyal trading yang akan dikirim ke Telegram.
    """
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    message = f"""📡 *SINYAL TRADING XAUUSD*

🕒 *Waktu:* {timestamp}
📊 *Trend H4:* {signal_data.get('trend', '-')}
📉 *Price:* ${signal_data.get('price', '-')}

🔍 *Analisa:*
- FVG H4: {signal_data.get('fvg_h4', '-')}
- FVG M15: {signal_data.get('fvg_m15', '-')}
- Order Block: {signal_data.get('ob', '-')}
- Break of Structure: {signal_data.get('bos', '-')}
- Liquidity Sweep: {signal_data.get('liquidity', '-')}

📈 *Konfirmasi:*
- EMA: {signal_data.get('ema', '-')}
- RSI: {signal_data.get('rsi', '-')}
- MACD: {signal_data.get('macd', '-')}
- Candle: {signal_data.get('candle', '-')}

⭐ *Rating Sinyal:* {signal_data.get('rating', '1')} dari 5
🔔 *Aksi:* {signal_data.get('action', '-')}
"""
    return message

def send_telegram_message(message):
    """
    Kirim pesan sinyal ke Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Sinyal berhasil dikirim ke Telegram.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengirim sinyal ke Telegram: {e}")

