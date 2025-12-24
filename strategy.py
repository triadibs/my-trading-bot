# strategy.py
def check_entry(df, i):

    # Trade only in trending regime (EMA slope)
    ema_fast = df['close'].ewm(span=20).mean()
    ema_slow = df['close'].ewm(span=50).mean()

    if ema_fast[i-1] < ema_slow[i-1]:
        bias = 'short'
    else:
        bias = 'long'

    # Must be volatile enough
    if df.loc[i-1,'ATR_norm'] < 0.9:
        return None

    # Look for liquidity sweep candle
    sweep = False

    # LONG setup: sweep low then strong close
    r = df.iloc[i-1]
    prev = df.iloc[i-2]

    if bias == 'long':
        if r['low'] < prev['low'] and r['close'] > prev['low']:
            sweep = True
    else:
        if r['high'] > prev['high'] and r['close'] < prev['high']:
            sweep = True

    if not sweep:
        return None

    # ENTRY CONFIRMATION candle
    c = df.iloc[i]
    body = abs(c['close'] - c['open'])
    rng = c['high'] - c['low']
    if rng == 0:
        return None

    if bias == 'long' and c['close'] > c['open'] and body/rng > 0.5:
        return 'long'
    if bias == 'short' and c['close'] < c['open'] and body/rng > 0.5:
        return 'short'

    return None
