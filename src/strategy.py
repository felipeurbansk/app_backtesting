import vectorbt as vbt
import pandas_ta as ta 

def execute_all_strategies(coin_prices, coin_code):
    print("Executing all strategies")

    # Carregar as médias móveis exponenciais (EMA)
    fast_ema, slow_ema = moving_average_strategy(coin_prices, coin_code)  # EMA

    # Carregar o MACD
    macd = macd_strategy(coin_prices, coin_code)

    # Carregar o RSI
    rsi = rsi_strategy(coin_prices, coin_code)

    # Calculando sinais de compra e venda
    return entry_exit_signals(fast_ema, slow_ema, macd, rsi)
    
    

def entry_exit_signals(fast_ema, slow_ema, macd, rsi):
    print("Calculando sinais de compra e venda...")

    # Condição de entrada: EMA rápida cruza acima da EMA lenta, MACD positivo e RSI não sobrecomprado
    entries = (fast_ema > slow_ema) & (macd.macd > macd.signal) & (rsi.rsi < 70)
    
    # Condição de saída: EMA rápida cruza abaixo da EMA lenta, MACD negativo e RSI não sobrevendido
    exits = (fast_ema < slow_ema) & (macd.macd < macd.signal) & (rsi.rsi > 30)

    return entries, exits
    

# Carregar as médias móveis exponenciais (EMA)
def moving_average_strategy(coin_prices, coin_code):
    print("Carregando médias móveis exponenciais de " + coin_code + "...")
    fast_ema = ta.ema(coin_prices, length=11)  # EMA rápida
    slow_ema = ta.ema(coin_prices, length=22)  # EMA lenta

    return fast_ema, slow_ema

# Carregar o MACD
def macd_strategy(coin_prices, coin_code):
    print("Carregando MACD de " + coin_code + "...")
    macd = vbt.MACD.run(coin_prices, fast_window=22, slow_window=26, signal_window=9)

    return macd

def rsi_strategy(coin_prices, coin_code):
    print("Carregando RSI de " + coin_code + "...")
    rsi = vbt.RSI.run(coin_prices, window=14)

    return rsi