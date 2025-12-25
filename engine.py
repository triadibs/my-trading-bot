import requests, pandas as pd
from indicators import add_indicators
from strategy import check_entry
from telegram import send
from config import *

LAST_SIGNAL_TIME = {}

def fetch(pair):
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={INTERVAL}"
    r = requests.get(url).json()
    key = list(r['result'].keys())[0]
    data = r['result'][key]

    df = pd.DataFrame(data, columns=[
        'timestamp','open','high','low','close','vwap','volume','count'
    ])
    df = df[['timestamp','open','high','low','close']]
    df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

def run():
    global LAST_SIGNAL_TIME

    for symbol, kraken_pair in PAIRS.items():

        df = fetch(kraken_pair)
        df = add_indicators(df).dropna().reset_index(drop=True)

        i = len(df) - 2
        signal_time = df.iloc[i]['timestamp']

        if LAST_SIGNAL_TIME.get(symbol) == signal_time:
            continue

    df = add_indicators(df).dropna().reset_index(drop=True)

    i = len(df)-2
    signal_time = df.iloc[i]['timestamp']

    if LAST_SIGNAL_TIME == signal_time:
        return

    sig = check_entry(df, i)
    if not sig:
        return

    row = df.iloc[i]
    atr = row['ATR']
    entry = row['close']

    if sig == 'long':
        sl = entry - STOP_ATR * atr
        tp = entry + TP_ATR * atr
    else:
        sl = entry + STOP_ATR * atr
        tp = entry - TP_ATR * atr

    msg = f"""
🚨 *{symbol} {INTERVAL}M SIGNAL*

Time : {signal_time}
Side : *{sig.upper()}*
Entry: `{entry:.2f}`
Stop : `{sl:.2f}`
TP   : `{tp:.2f}`

ATR : {atr:.2f}
Model: Liquidity Sweep
"""

    send(msg)
    LAST_SIGNAL_TIME[symbol] = signal_time

