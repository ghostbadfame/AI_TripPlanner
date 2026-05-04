import requests

from exceptions.exceptionHandling import ExternalServiceError, ValidationError

class CurrencyConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest"
    
    def convert(self, amount:float, from_currency:str, to_currency:str):
        """Convert the amount from one currency to another"""
        if not self.api_key:
            raise ExternalServiceError("Exchange Rate API key is not configured.")

        if amount < 0:
            raise ValidationError("Amount must be zero or greater.")

        if not from_currency or not to_currency:
            raise ValidationError("Both source and target currency codes are required.")

        source_currency = from_currency.strip().upper()
        target_currency = to_currency.strip().upper()
        url = f"{self.base_url}/{source_currency}"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as exc:
            raise ExternalServiceError(
                "Currency conversion service returned an error.",
                details={"from_currency": source_currency, "status_code": exc.response.status_code},
            ) from exc
        except requests.RequestException as exc:
            raise ExternalServiceError(
                "Unable to reach the currency conversion service.",
                details={"from_currency": source_currency},
            ) from exc

        rates = data.get("conversion_rates", {})
        if target_currency not in rates:
            raise ValidationError(f"{target_currency} not found in exchange rates.")

        return amount * rates[target_currency]
