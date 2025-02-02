import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    calc = Calculator()

    def test_evaluate_expression_valid(self):
        """Test that the evaluate_expression function works correctly."""
        value = "2×3"
        result = self.calc.display_frame.evaluate_expression(value)
        self.assertEqual(result, "6")

    def test_invalid_expressions(self):
        """Test that invalid expressions return 'Error'."""
        values = ["2÷0", "Error", None, "1e"]

        for value in values:
            result = self.calc.display_frame.evaluate_expression(value)
            self.assertEqual(result, "Error")



if __name__ == "__main__":
    unittest.main()