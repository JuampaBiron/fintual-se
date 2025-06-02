from stocks import Stock

class Portfolio:
    """
    Representa un portafolio de acciones con asignaciones a cada stock.
    Permite rebalancear basado en precios actuales del mercado.
    """
    
    def __init__(self, spend, allocations):
        """
        Inicializa el portfolio con dinero a invertir y allocations objetivo.
        
        Args:
            spend (float): Dinero total a invertir
            allocations (dict): Diccionario {símbolo: porcentaje} que debe sumar 1.0
        """
        # Validar que allocations sumen 1.0
        total_allocation = sum(allocations.values())
        if abs(total_allocation - 1.0) > 0.001:
            raise ValueError(f"Allocations must sum to 1.0, got {total_allocation:.3f}")
        
        self.total_investment = spend
        self.allocations = allocations.copy()
        self.stocks = {symbol: Stock(symbol) for symbol in allocations.keys()}
        self.holdings = self._calculate_initial_holdings()
    
    def _calculate_initial_holdings(self) -> dict: 
        """
        Calcula cuántas acciones comprar inicialmente basado en allocations.
        
        Returns:
            dict: {símbolo: cantidad_de_acciones}
        """
        holdings = {}
        
        for symbol, allocation in self.allocations.items():
            target_value = self.total_investment * allocation
            current_price = self.stocks[symbol].get_current_price()
            holdings[symbol] = target_value / current_price
        
        return holdings
    
    def get_portfolio_value(self) -> float:
        """
        Calcula el valor actual total del portafolio.
        
        Returns:
            float: Valor total actual del portafolio
        """
        total_value = 0
        for symbol, shares in self.holdings.items():
            current_price = self.stocks[symbol].get_current_price()
            total_value += shares * current_price
        
        return total_value
    
    def get_current_allocations(self):
        """
        Calcula las allocations actuales basadas en el valor actual.
        
        Returns:
            dict: {símbolo: porcentaje_actual}
        """
        total_value = self.get_portfolio_value()
        current_allocations = {}
        
        for symbol, shares in self.holdings.items():
            current_price = self.stocks[symbol].get_current_price()
            stock_value = shares * current_price
            current_allocations[symbol] = stock_value / total_value
        
        return current_allocations
    
    def rebalance(self, new_allocations)-> dict:
        """
        Calcula qué acciones vender y comprar para alcanzar las nuevas allocations.
        
        Args:
            new_allocations (dict): Nuevas allocations objetivo {símbolo: porcentaje}
        
        Returns:
            dict: {"to_sell": {símbolo: valor}, "to_buy": {símbolo: valor}}
        """
        # Validar que nuevas allocations sumen 1.0
        total_allocation = sum(new_allocations.values())
        if abs(total_allocation - 1.0) > 0.001:
            raise ValueError(f"New allocations must sum to 1.0, got {total_allocation:.3f}")
        
        current_portafolio_value = self.get_portfolio_value()
        to_sell = {}
        to_buy = {}
        
        for symbol, aiming_allocation in new_allocations.items():
            # Agregar nuevo stock si no existe
            if symbol not in self.stocks:
                self.stocks[symbol] = Stock(symbol)
                self.holdings[symbol] = 0
            
            aiming_value = current_portafolio_value * aiming_allocation
            current_shares = self.holdings.get(symbol, 0) 
            current_price = self.stocks[symbol].get_current_price()
            current_value = current_shares * current_price
            
            difference = aiming_value - current_value
            THRESHOLD = 1.0  # Umbral de dinero para evitar pequeñas transacciones
            if difference < -THRESHOLD:
                to_sell[symbol] = abs(difference) # Vender si el valor actual es mayor al objetivo
            elif difference > THRESHOLD:
                to_buy[symbol] = difference # Comprar si el valor actual es menor al objetivo
        
        return {"to_sell": to_sell, "to_buy": to_buy}


# Ejemplo de uso
if __name__ == "__main__":
    # Crear portfolio inicial
    portfolio = Portfolio(
        spend=10000,
        allocations={"META": 0.4, "AAPL": 0.6}
    )
    
    print(f"Creando portafolio: ${portfolio.total_investment:.2f} con allocations {portfolio.allocations}")

    # Rebalancear con nuevas allocations
    new_allocations = {"META": 0.3, "AAPL": 0.4, "TSLA": 0.3}
    print(f"Rebalance solicitado: {new_allocations}")
    rebalance_result = portfolio.rebalance(new_allocations)
    
    print("Rebalance necesario:")
    print("To sell:", rebalance_result["to_sell"])
    print("To buy:", rebalance_result["to_buy"])