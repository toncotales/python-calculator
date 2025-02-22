import re


WINDOW_HEIGHT = 350
WINDOW_WIDTH = 300
WINDOW_TITLE = "Calculator"
WINDOW_BACKGROUND_COLOR = "#5cbeff"

# https://www.flaticon.com/free-icon/calculator_9461186?related_id=9461186
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
FRAME_BORDER_COLOR = "#b3cde0"
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

def split_expression_with_exponents(expression):
    groups = []
    group = ''
    for i in expression:
        if i in OPERATORS:
            if group:
                if group[-1].casefold() in 'eE':
                    group += i
                else:
                    groups.append(group)
                    groups.append(i)
                    group = ''
        else:
            group += i
    if group:
        groups.append(group)
        group = ''

    return groups

def split_expression(expression):
	return re.split(r'([+–×÷\-/*])', expression)

def length_validator(value):
	return len(value) <= DISPLAY_LENGTH_LIMIT

def evaluate_expression(expression):
	"""
	Evaluates the given mathematical expression and returns the result or
	return 'Error' if the operation is invalid.
	"""
	result = expression
	try:
		expressions = split_expression(expression.translate(str.maketrans(OPERATOR_MAP)))

		if expression not in [ERROR, INITIAL_VALUE]:
			if len(expressions) > 2 and expressions[-1]:
				if not str(expressions[-1]).endswith('.'):

					# print(f'[OK] -> {''.join(expressions)}')

					result = eval(''.join(expressions))
					# print(f'Evaluation #1: {result}')

					# Combined regular expression patterns for finding numbers
					# with 10 or more trailing 9s or 0s
					combined_pattern = r'\b\d+\.\d*(9{10,}|0{10,})\b'
					round_ndigits = 15

					if any(re.findall(combined_pattern, str(result))):
						round_ndigits = 14

					result = round(result, ndigits=round_ndigits)
					# print(f'Evaluation #2: {result}')

					if len(str(result)) > DISPLAY_LENGTH_LIMIT:
						result = round(result, ndigits=4)

					if str(result).endswith('.0'):
						result = int(result)

					# print(f'Evaluation #3: {result}')

	except Exception as e:
		# print(f'Evaluation Error: {e}')
		result = ERROR

	return result