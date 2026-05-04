import os
from typing import List

from dotenv import load_dotenv
from langchain.tools import tool

from exceptions.exceptionHandling import AppException
from utils.currency_convertor import CurrencyConverter


class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY") or os.environ.get("EXCHANGHE_RATE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""

        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """Convert amount from one currency to another"""
            if not self.api_key:
                return (
                    "Currency converter is not configured. Add `EXCHANGE_RATE_API_KEY` or "
                    "`EXCHANGHE_RATE_API_KEY`. Until then, tell the user you cannot provide a "
                    "live exchange rate and only provide rough labeled estimates if needed."
                )
            try:
                return self.currency_service.convert(amount, from_currency, to_currency)
            except AppException as exc:
                return exc.message

        return [convert_currency]
