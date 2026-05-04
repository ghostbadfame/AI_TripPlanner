from exceptions.exceptionHandling import ValidationError


class Calculator:
    @staticmethod
    def _to_float(value: float | int | str) -> float:
        """Convert numeric strings like '1,200' into floats."""
        if isinstance(value, (int, float)):
            return float(value)

        if not isinstance(value, str) or not value.strip():
            raise ValidationError("A numeric value is required for this calculation.")

        cleaned = value.strip().replace(",", "")

        try:
            return float(cleaned)
        except ValueError as exc:
            raise ValidationError(
                "Invalid numeric value provided.",
                details={"value": value},
            ) from exc

    @classmethod
    def multiply(cls, a: float | int | str, b: float | int | str) -> float:
        """
        Multiply two numeric values.

        Args:
            a (float | int | str): The first numeric value.
            b (float | int | str): The second numeric value.

        Returns:
            float: The product of a and b.
        """
        return cls._to_float(a) * cls._to_float(b)
    
    @classmethod
    def calculate_total(cls, *x: float | int | str) -> float:
        """
        Calculate sum of the given numeric values.

        Args:
            x (tuple): Numeric values to sum.

        Returns:
            float: The sum of the numeric values.
        """
        return sum(cls._to_float(value) for value in x)
    
    @classmethod
    def calculate_daily_budget(cls, total: float | int | str, days: float | int | str) -> float:
        """
        Calculate daily budget.

        Args:
            total (float | int | str): Total cost.
            days (float | int | str): Total number of days.

        Returns:
            float: Expense for a single day.
        """
        total_value = cls._to_float(total)
        days_value = cls._to_float(days)
        if days_value <= 0:
            raise ValidationError("Number of days must be greater than zero.")
        return total_value / days_value
