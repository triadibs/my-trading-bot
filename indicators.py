# indicators.py

import pandas as pd
import numpy as np

def atr(df, period=20):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def add_indicators(df):
    df['ATR'] = atr(df, 20)
    df['ATR_norm'] = df['ATR'] / df['ATR'].rolling(96).mean()
    df['HH_20'] = df['high'].rolling(20).max()
    df['LL_20'] = df['low'].rolling(20).min()
    return df
