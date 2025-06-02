import finnhub
import os
from dotenv import load_dotenv

class Stock:
    """
    Representa una acción individual con su símbolo y precio actual.
    Utiliza Finnhub SDK para obtener precios reales de mercado.
    """
    
    _finnhub_client = None
    
    def __init__(self, symbol):
        """
        Inicializa un Stock con su símbolo.
        
        Args:
            symbol (str): Símbolo de la acción (ej: "META", "AAPL")
        """
        self.symbol = symbol.upper()
        
        # Inicializar cliente si no existe
        if Stock._finnhub_client is None:
            Stock._initialize_client()
    
    @classmethod
    def _initialize_client(cls):
        """Inicializa el cliente de Finnhub usando variables de entorno."""
        load_dotenv()
        api_key = os.getenv("FINNHUB_API_KEY")
        
        if not api_key:
            raise ValueError("FINNHUB_API_KEY not found in environment variables. Create a .env file with your API key.")
        
        cls._finnhub_client = finnhub.Client(api_key=api_key)
    
    def get_current_price(self):
        """
        Obtiene el precio actual de la acción desde Finnhub API. https://finnhub.io/docs/api/quote
        
        Returns:
            float: Precio actual de la acción
        """
        quote = self._finnhub_client.quote(self.symbol)
        
        if 'c' not in quote or quote['c'] is None or quote['c'] <= 0:
            raise ValueError(f"Invalid price data for {self.symbol}")
        current_price = float(quote['c'])
        return current_price
    def __str__(self):
        return f"Stock({self.symbol}: ${self.get_current_price():.2f})"
    
    def __repr__(self):
        return self.__str__()
    

if __name__ == "__main__":
    try:
        stock = Stock("AAPL")
        print(stock)
    except Exception as e:
        print(f"Error: {e}")
    
