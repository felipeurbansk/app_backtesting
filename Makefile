.PHONY: start

coin_code ?= BTCUSDT
interval ?= 1h
days_interval ?= 29

start:
	python3 main.py --coin_code=$(coin_code) --interval=$(interval) --days_interval=$(days_interval)