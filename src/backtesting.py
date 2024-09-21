import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import argparse

from src.data_loader import load_data
from src.strategy import execute_all_strategies
from src.report import create_portfolio_report
from src.utils import get_start_date

load_dotenv()

# Inicializar a aplicação
def main():
    parser = argparse.ArgumentParser(description="Processa os parâmetros do Makefile")
    parser.add_argument('--interval', type=str, required=False, help='Intervalo de tempo, ex: 1h')
    parser.add_argument('--days_interval', type=int, required=False, help='Intervalo de dias, ex: 29')
    parser.add_argument('--coin_code', type=str, required=False, help='Código da moeda, ex: BTCUSDT')
    
    args = parser.parse_args()

    # Definir o intervalo de dias a serem analisados
    days_interval = int(args.days_interval or os.getenv('START_DAYS_INTERVAL', 29))

    # Definir o código da moeda
    coin_code = args.coin_code or 'BTCUSDT'

    # Definir o intervalo de tempo
    interval = args.interval or '1h'

    # Definir a data de início
    start = get_start_date(days_interval)

    # Definir o filtro da moeda
    coin_filter = coin_code + '_' + interval + '_' + start

    # Configuração do Backtesting
    initial_value = 100  # Valor inicial do portfólio
    fees_percent = 0.0025  # Taxa de transação de 0.25%

    # Definir o nome do arquivo que contém os dados históricos da moeda
    coin_price = load_data(coin_code, interval, start, coin_filter)

    # Executar todas as estratégias
    entries, exits = execute_all_strategies(coin_price, coin_code)

    # Criar relatório do portfólio
    create_portfolio_report(
        coin_code, 
        coin_price, 
        entries, 
        exits, 
        initial_value, 
        fees_percent, 
        coin_filter
    )

# Executa o script apenas se o arquivo for executado diretamente
if __name__ == '__main__':
    main()