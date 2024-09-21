from datetime import datetime, timedelta

def get_start_date(days_interval):
    return (datetime.now() - timedelta(days=days_interval)).strftime('%Y-%m-%d')