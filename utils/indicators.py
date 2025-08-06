import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hitung indikator teknikal utama: EMA, MACD, RSI dan tambahkan ke DataFrame.
    """

    # EMA
    df["ema_20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
    df["ema_50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
    
    # RSI
    df["rsi_14"] = RSIIndicator(close=df["close"], window=14).rsi()
    
    # MACD
    macd = MACD(close=df["close"])
    df["macd_line"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    return df

def detect_fvg(df: pd.DataFrame, lookback: int = 50) -> list:
    """
    Deteksi Fair Value Gaps (FVG) dalam data OHLC.
    Return: List berisi dictionary detail FVG.
    """
    fvg_list = []
    for i in range(2, min(len(df), lookback)):
        high_2 = df.iloc[i - 2]['high']
        low_0 = df.iloc[i]['low']
        low_2 = df.iloc[i - 2]['low']
        high_0 = df.iloc[i]['high']
        body_1 = df.iloc[i - 1]

        # FVG Bullish
        if low_0 > high_2:
            fvg_list.append({
                "index": df.index[i],
                "type": "bullish",
                "gap_above": high_2,
                "gap_below": low_0
            })

        # FVG Bearish
        if high_0 < low_2:
            fvg_list.append({
                "index": df.index[i],
                "type": "bearish",
                "gap_above": high_0,
                "gap_below": low_2
            })

    return fvg_list

def is_trending_up(df: pd.DataFrame) -> bool:
    """
    Cek apakah tren sedang naik berdasarkan EMA.
    """
    if df["ema_20"].iloc[-1] > df["ema_50"].iloc[-1]:
        return True
    return False

def is_trending_down(df: pd.DataFrame) -> bool:
    """
    Cek apakah tren sedang turun berdasarkan EMA.
    """
    if df["ema_20"].iloc[-1] < df["ema_50"].iloc[-1]:
        return True
    return False

def macd_crossover(df: pd.DataFrame) -> str:
    """
    Deteksi MACD crossover terakhir (bullish/bearish).
    """
    if df["macd_line"].iloc[-1] > df["macd_signal"].iloc[-1] and df["macd_line"].iloc[-2] < df["macd_signal"].iloc[-2]:
        return "bullish"
    elif df["macd_line"].iloc[-1] < df["macd_signal"].iloc[-1] and df["macd_line"].iloc[-2] > df["macd_signal"].iloc[-2]:
        return "bearish"
    return "none"

def rsi_status(df: pd.DataFrame) -> str:
    """
    Evaluasi kondisi RSI terakhir.
    """
    rsi = df["rsi_14"].iloc[-1]
    if rsi > 70:
        return "overbought"
    elif rsi < 30:
        return "oversold"
    else:
        return "neutral"

