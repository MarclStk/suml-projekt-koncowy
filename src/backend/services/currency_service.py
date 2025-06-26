
import requests
from datetime import datetime
from typing import Dict, List, Optional
from forex_python.converter import CurrencyRates


class CurrencyService:
    
    def __init__(self):
        self.currency_rates = CurrencyRates()
        self.available_currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", 
            "CAD", "CHF", "CNY", "SEK", "NZD",
            "PLN", "CZK", "HUF", "NOK", "DKK"
        ]
    
    def get_available_currencies(self) -> List[str]:
        return self.available_currencies
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return amount
            
        try:
            exchange_rate = self.currency_rates.get_rate(from_currency, to_currency)

            converted_amount = amount * exchange_rate
            
            return converted_amount
        except Exception as e:
            print(f"Error in currency conversion: {e}")
            return self._convert_via_api(amount, from_currency, to_currency)
    
    def _convert_via_api(self, amount: float, from_currency: str, to_currency: str) -> float:
        try:
            url = f"https://open.er-api.com/v6/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            
            if data.get("result") == "success":
                exchange_rate = data["rates"].get(to_currency)
                if exchange_rate:
                    return amount * exchange_rate
            
            return amount
        except Exception:
            return amount
    
    def get_currency_symbol(self, currency_code: str) -> str:
        symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "AUD": "A$",
            "CAD": "C$",
            "CHF": "CHF",
            "CNY": "¥",
            "SEK": "kr",
            "NZD": "NZ$",
            "PLN": "zł",
            "CZK": "Kč",
            "HUF": "Ft",
            "NOK": "kr",
            "DKK": "kr"
        }
        
        return symbols.get(currency_code, currency_code)
