import re


WINDOW_HEIGHT = 350
WINDOW_WIDTH = 300
WINDOW_TITLE = "Calculator"
WINDOW_BACKGROUND_COLOR = "#5cbeff"

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

DISPLAY_LENGTH_LIMIT = 17
DISPLAY_FONT = ("Default", 20, "normal")
DISPLAY_FOREGROUND_COLOR = "#393e46"

BUTTON_FONT = ("Verdana", 12, "normal")
# Button configuration: (text label, row position, column position)
BUTTONS = [
			('C', 0, 0), ('←', 0, 1), ('%', 0, 2), ('÷', 0, 3),
			('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
			('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('–', 2, 3),
			('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
			('0', 4, 0), ('.', 4, 2), ('=', 4, 3)
        ]


SCIENTIFIC_NOTATION = "e"
INITIAL_VALUE = "0"
ERROR = "Error"
OPERATORS = "+–×÷-*/"
OPERATOR_MAP = dict(zip("+–×÷", "+-*/"))


def split_expression(expression):
	return re.split(r'([+–×÷\-/*])', expression)

def length_validator(value):
	return len(value) <= DISPLAY_LENGTH_LIMIT



def evaluate_expression(expression):
	"""
	Evaluates the given mathematical expression and returns the result or
	return 'Error' if the operation is invalid.
	"""
	# TODO: Need to refactor the logic on this functionality
	if expression not in [ERROR, INITIAL_VALUE]:
		try:
			expression = expression.translate(str.maketrans(OPERATOR_MAP))
			base_expressions = split_expression(expression)

			if len(base_expressions) > 2 and base_expressions[-1]:

				result = eval(expression)

				# Find trailing nines and zeros in evaluation result
				nines = re.findall(r'\b\d+\.\d*9{10,}\b', str(result))
				zeros = re.findall(r'\b\d+\.\d*0{10,}\b', str(result))
				if any(nines + zeros):
					round_ndigits = 14
				else:
					round_ndigits = 15
				# Round the result to 14 decimal places for precision
				result = round(result, ndigits=round_ndigits)

				if str(result).endswith('.0'):
					result = int(result)
			else:
				print(f'testing: {expression}')
				result = expression
				print(f'testing: {result}')

		except Exception as e:
			print(f'Error: {e}')
			result = ERROR

		# print(f'result: {result}')
		return result