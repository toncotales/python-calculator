import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    # TODO: Need to remake this unittest file
    pass

    # def test_evaluate_expression_valid(self):
    #     """Test that the evaluate_expression function works correctly."""
    #     calc = Calculator()
    #     value = "2×3"
    #     result = calc.widget_frame.evaluate_expression(value)
    #     self.assertEqual(result, "6")
    #     calc.destroy()

    # def test_invalid_expressions(self):
    #     """Test that invalid expressions return 'Error'."""
    #     calc = Calculator()
    #     values = ["2÷0", "Error", None, "1e"]
    #     for value in values:
    #         result = calc.widget_frame.evaluate_expression(value)
    #         self.assertEqual(result, "Error")
    #     calc.destroy()

    # def test_process_insert(self):
    #     """Test the input process functionality for button clicks or keyboard presses."""
    #     calc = Calculator()
    #     values = ".2×.8"
    #     result = "0.2×0.8"
    #     for value in values:
    #         calc.widget_frame.process_insert(value)
    #     self.assertEqual(calc.widget_frame.display.get(), result)
    #     calc.destroy()

    # def test_invalid_inputs(self):
    #     """Test the input functionality for invalid keyboard presses."""
    #     calc = Calculator()
    #     values = "abcdefghijklmnopqrstuvwxyz"
    #     for value in values:
    #         calc.widget_frame.process_insert(value) # Invalid input
    #         self.assertEqual(calc.widget_frame.display.get(), "0")  # It should remain 0
    #     calc.destroy()
            
    # def test_clear_display(self):
    #     """Test the clear display functionality."""
    #     calc = Calculator()
    #     calc.widget_frame.process_insert("45678")  # Valid input numbers
    #     calc.widget_frame.process_insert("\x1b")  # C or the ESC key press
    #     self.assertEqual(calc.widget_frame.display.get(), "0")
    #     calc.destroy()

    # def test_backspace_function(self):
    #     """Test that backspace works as expected."""
    #     calc = Calculator()
    #     backspaces = ['←', '\x08']  # Either button click or the backspace key press
    #     calc.widget_frame.process_insert("12")
    #     for backspace in backspaces:
    #         calc.widget_frame.process_insert(backspace)
    #     self.assertEqual(calc.widget_frame.display.get(), "0")
    #     calc.destroy()
             
if __name__ == "__main__":
    unittest.main()