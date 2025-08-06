import pandas as pd


def is_bullish(candle):
    return candle['close'] > candle['open']


def is_bearish(candle):
    return candle['close'] < candle['open']


def detect_bullish_engulfing(df):
    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return is_bearish(prev) and is_bullish(curr) and \
        curr['close'] > prev['open'] and curr['open'] < prev['close']


def detect_bearish_engulfing(df):
    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return is_bullish(prev) and is_bearish(curr) and \
        curr['close'] < prev['open'] and curr['open'] > prev['close']


def detect_pinbar(df, body_ratio_threshold=0.3):
    if len(df) < 1:
        return None

    candle = df.iloc[-1]
    body = abs(candle['close'] - candle['open'])
    candle_range = candle['high'] - candle['low']

    if candle_range == 0:
        return None  # Hindari pembagian 0

    body_ratio = body / candle_range

    upper_wick = candle['high'] - max(candle['close'], candle['open'])
    lower_wick = min(candle['close'], candle['open']) - candle['low']

    if body_ratio < body_ratio_threshold:
        if upper_wick > 2 * body:
            return 'bearish_pinbar'
        elif lower_wick > 2 * body:
            return 'bullish_pinbar'

    return None


def detect_price_action_signals(df):
    signals = []

    if detect_bullish_engulfing(df):
        signals.append('Bullish Engulfing')

    if detect_bearish_engulfing(df):
        signals.append('Bearish Engulfing')

    pinbar = detect_pinbar(df)
    if pinbar == 'bullish_pinbar':
        signals.append('Bullish Pinbar')
    elif pinbar == 'bearish_pinbar':
        signals.append('Bearish Pinbar')

    return signals

