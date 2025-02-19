import re


WINDOW_HEIGHT = 350
WINDOW_WIDTH = 300
WINDOW_TITLE = "Calculator"
WINDOW_BACKGROUND_COLOR = "#5cbeff"

SCIENTIFIC_NOTATION = "e"

DISPLAY_INITIAL_VALUE = "0"
DISPLAY_ERROR = "Error"
DISPLAY_FONT = ("Default", 20, "normal")
DISPLAY_FOREGROUND_COLOR = "#393e46"
DISPLAY_OPERATORS = "+–×÷"

PYTHON_OPERATORS = "+-*/"

OPERATOR_MAP = dict(zip(DISPLAY_OPERATORS, PYTHON_OPERATORS))

BUTTON_FONT = ("Verdana", 12, "normal")

# Button configuration: (text label, row position, column position)
BUTTONS = [
			('C', 1, 0), ('←', 1, 1), ('%', 1, 2), ('÷', 1, 3),
			('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
			('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('–', 5, 3),
			('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('+', 7, 3),
			('0', 9, 0), ('.', 9, 2), ('=', 9, 3)
        ]

BUTTONS2 = [
			('C', 0, 0), ('←', 0, 1), ('%', 0, 2), ('÷', 0, 3),
			('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
			('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('–', 2, 3),
			('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
			('0', 4, 0), ('.', 4, 2), ('=', 4, 3)
        ]

WINDOW_ICON = """\
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAB2AAAAdgFOey\
YIAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAgtJREFUOI19kj1MU1\
EYhp9zem+92oJAowjEmoiBKAZ/iIbJRk1MaCKTicaA0Q4mLi510ejm5EDipi4ODibGjbjqpoMaSU\
wKBMtfpLVQpaW0tL33nuMAEgvcvtM55/veJ+/35Qg2dGHoyWkh3CtCSEkdKbTG54y+f/nwI4Cx\
WZHuiC+wN+Lf1+5pzu1qQWRmqKZnbgJttQCkETjaR+D4WU9AahlWmztpSr/Ys+mq6RCiXno\
QoHXtUy1ga3WrNCBqe4z/L8Xxr9jZ9Daf0ppypYq0QjSkp+skKBfpCVY4JPKszU7QZZXoskpkx8c\
4SI5+YwEjl/IGdLQ2cffGJe5cv4jfNIjHBojHBjAMSTwW5f7tQcJtLd4jFIplkvOLLP0p4CpFIplCKYXj\
KhI/FtgfamRldc0bUK06JJIpVgolbNvl++Q8GtBK83PiMaWGInblDLB75xFCzUEunz9JNHICR9lcjfZ\
zLdqPafoYPveFW5HPHGjOeyfILhcY/fCNxd95yhWH1+8+AWDbLmawD1pOAUveS7T8Jsc62+k+\
3IaQgt7uML3dYYQUuJU5KI+xVTUJLMukM9xKU2MAn5T0HOkAwCclys5CaRb00M4ArZQ7NZfh0\
dO3lNaqVG2HByNv1pdrO9x7NUjQqjCdCQFCbQOUXfeZRvsTyfWPYhoGk7O/Ns9TmY6NoTWGlM\
//+f4CrqzDeV+thpcAAAAASUVORK5CYII=\
"""

def get_base_expression(expression):
	pattern = r'([+–×÷\-/*])'
	return re.split(pattern, expression)


def evaluate_expression(expression):
	"""
	Evaluates the given mathematical expression and returns the result or
	return 'Error' if the operation is invalid.
	"""
	try:
		expression = expression.translate(str.maketrans(OPERATOR_MAP))
		base = get_base_expression(expression)
		print(f'Base: {base}')
		if len(base) > 2 and base[-1]:

			print('Expression can be processed!')
			result = eval(expression)
			print(f'TEST RESULT: {result}')

			# If the result is None (invalid expression), set it to 'Error'
			if isinstance(result, type(None)):
				raise Exception

			# Round the result to 14 decimal places for precision
			result = round(result, ndigits=14)

	except (SyntaxError, ZeroDivisionError, Exception) as e:
		raise

	print(f'Expression: {expression}')
	return expression