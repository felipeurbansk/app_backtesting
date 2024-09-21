import os
import vectorbt as vbt

folder_plots = os.getenv('APPLICATION_PLOTS', 'plots')

def create_portfolio_report(coin_code, coin_price, entries, exits, initial_value, fees_percent, coin_filter):
    print("Criando relatório do portfólio...")
    os.makedirs(folder_plots, exist_ok=True)

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