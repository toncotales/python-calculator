import unittest
from config import evaluate_expression, ERROR
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(evaluate_expression("2+2"), 4)
        self.assertEqual(evaluate_expression("10-3"), 7)
        self.assertEqual(evaluate_expression("4*5"), 20)
        self.assertEqual(evaluate_expression("20/4"), 5)

    def test_complex_operations(self):
        self.assertEqual(evaluate_expression("3+5*2"), 13)
        self.assertEqual(evaluate_expression("2+3*4"), 14)
        self.assertEqual(evaluate_expression("10/2+3"), 8)

    def test_division_by_zero(self):
        self.assertEqual(evaluate_expression("5/0"), ERROR)

    def test_invalid_expression(self):
        self.assertEqual(evaluate_expression("5+e+3"), ERROR)
        self.assertEqual(evaluate_expression("abc+3"), ERROR)
        self.assertEqual(evaluate_expression("2..3+1"), ERROR)

    def test_percentage(self):
        self.assertEqual(evaluate_expression("50/100"), 0.5)
        self.assertEqual(evaluate_expression("200*50/100"), 100)

    def test_gui_button_clicks(self):

        app = Calculator()

        app.calc.display.configure(state='normal')
        
        app.calc.process_insert("1")
        self.assertEqual(app.calc.display.get(), "1")
        
        app.calc.process_insert("+")
        self.assertEqual(app.calc.display.get(), "1+")
        
        app.calc.process_insert("2")
        self.assertEqual(app.calc.display.get(), "1+2")
        
        app.calc.equalsign_handler()
        self.assertEqual(app.calc.display.get(), "3")
        
        app.calc.clear_display()
        self.assertEqual(app.calc.display.get(), "0")

        app.close()
        
    
    def test_gui_keypresses(self):

        app = Calculator()

        app.calc.display.configure(state='normal')
        
        app.calc.process_insert("5")
        app.calc.process_insert("*")
        app.calc.process_insert("3")
        
        self.assertEqual(app.calc.display.get(), "5*3")
        
        app.calc.equalsign_handler()
        self.assertEqual(app.calc.display.get(), "15")
        
        app.calc.process_insert("←")  # Simulate backspace
        self.assertEqual(app.calc.display.get(), "1")
        
        app.calc.clear_display()
        self.assertEqual(app.calc.display.get(), "0")

        app.close()


if __name__ == "__main__":
    unittest.main()
