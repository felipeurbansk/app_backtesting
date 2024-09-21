import os
from dotenv import load_dotenv
import vectorbt as vbt
import pandas as pd
import pandas_ta as ta 
from datetime import datetime, timedelta

load_dotenv()

# Inicializar a aplicação
def main():
    # Definir o caminho da pasta de dados
    folder_path = os.getenv('APPLICATION_DATA', 'src/data')
    folder_plots = os.getenv('APPLICATION_PLOTS', 'src/plots')

    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(folder_plots, exist_ok=True)

    # Definir o intervalo de dias para carregar os dados
    days_interval = int(os.getenv('START_DAYS_INTERVAL', 29))

    # Definir o código da moeda, intervalo de tempo e data de início
    coin_code = 'AAVEBTC' # Código da moeda
    interval = '1h'  # Intervalo
    start = (datetime.now() - timedelta(days=days_interval)).strftime('%Y-%m-%d')

    # Backtesting
    initial_value = 100  # Valor inicial do portfólio
    fees_percent = 0.0025  # Taxa de transação de 0.25%

    # Definir o nome do arquivo que contém os dados históricos da moeda
    coin_filter = coin_code + '_' + interval + '_' + start
    file_name = os.path.join(folder_path, coin_code, coin_filter + '.csv')

    if not os.path.exists(os.path.join(folder_path, coin_code)):
        os.makedirs(os.path.join(folder_path, coin_code))

    if os.path.exists(file_name):
        print("Arquivo de dados de " + coin_code + " encontrado!")
        coin_price = pd.read_csv(file_name, index_col=0, parse_dates=True)
    else:
        # vbt.settings.data.binance['api_key'] = os.getenv('BINANCE_API_KEY')
        # vbt.settings.data.binance['api_secret'] = os.getenv('BINANCE_API_SECRET')

        coin_price = vbt.BinanceData.download(
            coin_code,
            interval = interval,
            start = start + 'UTC'
        ).get('Close')

        if coin_price.empty:
            print(f"Nenhum dado encontrado para {coin_code} desde {start}")
            return

        print(f"Salvando dados em {file_name}...")

        coin_price.to_csv(file_name)
        print("Dados de " + coin_code + " salvos com sucesso!")

        coin_price = pd.read_csv(file_name, index_col=0, parse_dates=True)

    if coin_price.empty:
        print(f"Nenhum dado carregado para {coin_code}.")
        return

    print("Garantindo que os dados estão no formato correto...")
    if 'Close' in coin_price.columns:
        coin_price = coin_price['Close'] 

    # Carregar as médias móveis exponenciais (EMA)
    print("Carregando médias móveis exponenciais de " + coin_code + "...")
    fast_ema = ta.ema(coin_price, length=11)  # EMA rápida
    slow_ema = ta.ema(coin_price, length=22)  # EMA lenta

    # Carregar o MACD
    print("Carregando MACD de " + coin_code + "...")
    macd = vbt.MACD.run(coin_price, fast_window=22, slow_window=26, signal_window=9)

    # Carregar o RSI
    print("Carregando RSI de " + coin_code + "...")
    rsi = vbt.RSI.run(coin_price, window=14)

    # Calculando sinais de compra e venda
    print("Calculando sinais de compra e venda...")
    
    # Condição de entrada: EMA rápida cruza acima da EMA lenta, MACD positivo e RSI não sobrecomprado
    entries = (fast_ema > slow_ema) & (macd.macd > macd.signal) & (rsi.rsi < 70)
    
    # Condição de saída: EMA rápida cruza abaixo da EMA lenta, MACD negativo e RSI não sobrevendido
    exits = (fast_ema < slow_ema) & (macd.macd < macd.signal) & (rsi.rsi > 30)

    # Calcular o portfólio
    print("Calculando o portfólio...")
    portfolio = vbt.Portfolio.from_signals(coin_price, entries, exits, init_cash=initial_value, fees=fees_percent)

    print("Plotando o portfólio...")
    plot_dir = os.path.join(folder_plots, coin_code, coin_filter)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    portfolio.plot().write_html(
        plot_dir  + '/portfolio.html'
    )
    print(f"Gráfico salvo como { plot_dir  + '/portfolio.html' }")

    print("Calculando estatísticas do portfólio...")
    stats = portfolio.stats()

    print("Estatísticas do portfólio:")
    print(stats)

# Executa o script apenas se o arquivo for executado diretamente
if __name__ == '__main__':
    main()