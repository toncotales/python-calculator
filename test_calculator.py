import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    calc = Calculator()

    def test_evaluate_expression_valid(self):
        """Test that the evaluate_expression function works correctly."""
        value = "2×3"
        result = self.calc.widget_frame.evaluate_expression(value)
        self.assertEqual(result, "6")

    def test_invalid_expressions(self):
        """Test that invalid expressions return 'Error'."""
        values = ["2÷0", "Error", None, "1e"]
        for value in values:
            result = self.calc.widget_frame.evaluate_expression(value)
            self.assertEqual(result, "Error")

    def test_process_input(self):
        """Test the input process functionality for button clicks or keyboard presses."""
        values = ".2×.8"
        result = "0.2×0.8"
        for value in values:
            self.calc.widget_frame.process_input(value)
        self.assertEqual(self.calc.widget_frame.display.get(), result)

    def test_invalid_inputs(self):
        """Test the input functionality for invalid keyboard presses."""
        values = "abcdefghijklmnopqrstuvwxyz"
        for value in values:
            self.calc.widget_frame.process_input(value) # Invalid input
            self.assertEqual(self.calc.widget_frame.display.get(), "0")  # It should remain 0
            
    def test_clear_display(self):
        """Test the clear display functionality."""
        self.calc.widget_frame.process_input("45678")  # Valid input numbers
        self.calc.widget_frame.process_input("\x1b")  # C or the ESC key press
        self.assertEqual(self.calc.widget_frame.display.get(), "0")

    def test_backspace_function(self):
        """Test that backspace works as expected."""
        backspaces = ['←', '\x08']  # Either button click or the backspace key press
        self.calc.widget_frame.process_input("12")
        for backspace in backspaces:
            self.calc.widget_frame.process_input(backspace)
        self.assertEqual(self.calc.widget_frame.display.get(), "0")



if __name__ == "__main__":
    unittest.main()