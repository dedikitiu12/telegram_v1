
def detect_order_block(data):
    """
    Deteksi order block sederhana berdasarkan candle besar dan imbalance harga.
    - Bullish OB: candle hijau besar sebelum pergerakan naik signifikan.
    - Bearish OB: candle merah besar sebelum pergerakan turun signifikan.
    """
    order_blocks = []

    for i in range(2, len(data) - 2):
        body = abs(data['close'][i] - data['open'][i])
        prev_body = abs(data['close'][i - 1] - data['open'][i - 1])
        next_body = abs(data['close'][i + 1] - data['open'][i + 1])

        is_bullish_ob = (
            data['close'][i] > data['open'][i] and
            body > prev_body * 1.5 and
            data['close'][i + 1] > data['high'][i]
        )

        is_bearish_ob = (
            data['close'][i] < data['open'][i] and
            body > prev_body * 1.5 and
            data['close'][i + 1] < data['low'][i]
        )

        if is_bullish_ob:
            order_blocks.append({
                'type': 'bullish',
                'index': i,
                'price': data['open'][i]
            })

        elif is_bearish_ob:
            order_blocks.append({
                'type': 'bearish',
                'index': i,
                'price': data['open'][i]
            })

    return order_blocks


def detect_fvg(data):
    """
    Deteksi Fair Value Gap (FVG):
    - Terjadi ketika low candle ke-0 > high candle ke-2 (untuk bullish FVG)
    - Atau high candle ke-0 < low candle ke-2 (untuk bearish FVG)
    """
    fvg_zones = []

    for i in range(2, len(data)):
        prev2_high = data['high'][i - 2]
        prev2_low = data['low'][i - 2]
        prev1_high = data['high'][i - 1]
        prev1_low = data['low'][i - 1]
        curr_high = data['high'][i]
        curr_low = data['low'][i]

        # Bullish FVG
        if prev2_low > curr_high:
            fvg_zones.append({
                'type': 'bullish',
                'index': i,
                'gap_low': curr_high,
                'gap_high': prev2_low
            })

        # Bearish FVG
        elif prev2_high < curr_low:
            fvg_zones.append({
                'type': 'bearish',
                'index': i,
                'gap_high': curr_low,
                'gap_low': prev2_high
            })

    return fvg_zones
