import vectorbt as vbt
import os
import pandas as pd

folder_path = os.getenv('APPLICATION_DATA', 'data')

def load_data(coin_code, interval, start, coin_filter):
    print("Carregando dados de " + coin_code + "...")
    os.makedirs(folder_path, exist_ok=True)

    # Definir o nome do arquivo que contém os dados históricos da moeda
    file_name = os.path.join(folder_path, coin_code, coin_filter + '.csv')

    if not os.path.exists(os.path.join(folder_path, coin_code)):
        os.makedirs(os.path.join(folder_path, coin_code))

    if os.path.exists(file_name):
        print("Arquivo de dados " + coin_code + " encontrado!")
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

        print("Dados de " + coin_code + " salvos com sucesso em " + file_name)
        coin_price = pd.read_csv(file_name, index_col=0, parse_dates=True)

    if coin_price.empty:
        print(f"Nenhum dado carregado para {coin_code}.")
        return
    
    print("Garantindo que os dados estão no formato correto...")
    if 'Close' in coin_price.columns:
        coin_price = coin_price['Close'] 

    return coin_price