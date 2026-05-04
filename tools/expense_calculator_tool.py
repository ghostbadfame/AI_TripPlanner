from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool
from exceptions.exceptionHandling import AppException

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(
            price_per_night: float | int | str,
            total_days: float | int | str,
        ) -> float:
            """Calculate total hotel cost"""
            try:
                return self.calculator.multiply(price_per_night, total_days)
            except AppException as exc:
                return exc.message
        
        @tool
        def calculate_total_expense(costs: list[float | int | str]) -> float:
            """Calculate total expense of the trip"""
            if not costs:
                return "At least one cost is required to calculate the total expense."
            try:
                return self.calculator.calculate_total(*costs)
            except AppException as exc:
                return exc.message
        
        @tool
        def calculate_daily_expense_budget(total_cost: float | int | str, days: float | int | str) -> float:
            """Calculate daily expense"""
            try:
                return self.calculator.calculate_daily_budget(total_cost, days)
            except AppException as exc:
                return exc.message
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]
