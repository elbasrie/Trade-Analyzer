import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import pytz

# Fungsi untuk mengambil dan menganalisis data
def analyze_crypto(symbol, interval='5m', period='1d'):
    # Mengambil data OHLCV dari yfinance
    data = yf.download(symbol, interval=interval, period=period)
    
    # Konversi ke zona waktu GMT+7
    tz = pytz.timezone('Asia/Bangkok')  # GMT+7
    data.index = data.index.tz_convert(tz)
    
    # Menghitung indikator teknikal
    # 1. RSI (Relative Strength Index)
    rsi_period = 14
    rsi = RSIIndicator(data['Close'], window=rsi_period).rsi()
    
    # 2. MACD (Moving Average Convergence Divergence)
    macd = MACD(data['Close']).macd()
    signal = MACD(data['Close']).macd_signal()
    
    # 3. Bollinger Bands
    bb = BollingerBands(data['Close'], window=20, window_dev=2)
    data['bb_mavg'] = bb.bollinger_mavg()
    data['bb_high'] = bb.bollinger_hband()
    data['bb_low'] = bb.bollinger_lband()
    
    # Menambahkan indikator ke DataFrame
    data['RSI'] = rsi
    data['MACD'] = macd
    data['Signal'] = signal
    
    # Analisis Indikator
    # Sinyal beli potensial
    buy_signal = []
    for i in range(1, len(data)):
        if data['RSI'][i] < 30 and data['MACD'][i] > data['Signal'][i]:
            buy_signal.append(data.index[i])
    
    # Plot hasil analisis
    plt.figure(figsize=(14, 7))
    
    # Plot harga dan Bollinger Bands
    plt.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(data.index, data['bb_mavg'], label='Bollinger MAVG', color='black', linestyle='--')
    plt.plot(data.index, data['bb_high'], label='Bollinger High', color='red', linestyle='--')
    plt.plot(data.index, data['bb_low'], label='Bollinger Low', color='green', linestyle='--')
    
    # Plot sinyal beli
    plt.scatter(buy_signal, data.loc[buy_signal]['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
    
    plt.title(f'{symbol} {interval} Chart Analysis (GMT+7)')
    plt.xlabel('Date (GMT+7)')
    plt.ylabel('Price (USD)')
    plt.legend(loc='best')
    plt.grid()
    plt.show()
    
    # Menampilkan indikator
    print(data[['RSI', 'MACD', 'Signal']].tail())
    
    # Analisis kesimpulan
    if not buy_signal:
        print("Tidak ada sinyal beli yang ditemukan berdasarkan indikator RSI dan MACD.")
    else:
        print("Sinyal beli ditemukan pada:")
        for signal in buy_signal:
            print(signal)

# Input dari pengguna
symbol = input("Masukkan simbol koin (misalnya, 'SOL-USD' untuk Solana/USD): ")
#interval = input("Masukkan interval data (Default, '5m' untuk 5 menit): ")
#period = input("Masukkan periode data (Default, '1d' untuk 1 hari): ")

# Memanggil fungsi untuk analisis
analyze_crypto(symbol)
