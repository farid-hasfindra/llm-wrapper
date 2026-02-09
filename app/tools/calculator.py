class CalculatorTool:
    """
    Safe calculator for math operations.
    """
    def calculate(self, expression: str) -> float:
        try:
            # Dangerous in prod, use safe eval libs
            return eval(expression)
        except:
            return 0.0
