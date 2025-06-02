# Portafolio Manager

Clase que nos ayuda a rebalancear portafolios de acciones.

## Instalación

```bash
pip install finnhub-python python-dotenv
```

## Configuración

1. Regístrate en [finnhub.io](https://finnhub.io) (es gratis)
2. Crea archivo `.env`:

```
FINNHUB_API_KEY = tu_api_key
```

## Uso

```python
from portfolio import Portfolio

# Crear portfolio
portfolio = Portfolio(
    spend=10000,
    allocations={"AAPL": 0.6, "META": 0.4}
)

# Ver valor actual
print(f"Valor: ${portfolio.get_portfolio_value():.2f}")

# Rebalancear
result = portfolio.rebalance({"AAPL": 0.5, "META": 0.3, "TSLA": 0.2})
print("Vender:", result["to_sell"])
print("Comprar:", result["to_buy"])
```

## Archivos

- `stocks.py` - Manejo de precios via Finnhub API
- `portfolio.py` - Lógica de rebalanceo  
- `.env` - Tu API key

## Notas

- Solo rebalancea diferencias > $1
- Soporta acciones fraccionarias
- Los allocations deben sumar 1.0