import re
import config
import tkinter as tk
from tkinter import PhotoImage



class Calculator(tk.Tk):
	"""
	A simple and user-friendly calculator built using Python and Tkinter.

	Created by: Anthony Cotales
	Email: ton.cotales@gmail.com
	Version: 1.0.0
	"""

	def __init__(self):
		super().__init__()

		# Set window title, minimum and maximum size, and icon
		self.title(config.WINDOW_TITLE)
		self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}')
		self.minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
		self.maxsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
		self.iconphoto(False, PhotoImage(data=config.WINDOW_ICON))

		# Configure the row and column layout (useful for when adding widgets)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		# Set window background color
		self.configure(bg=config.WINDOW_BACKGROUND_COLOR)

		# Create a frame for the calculator widgets (e.g., buttons and display)
		self.display_frame = DisplayFrame(self, relief='groove', bg=config.WINDOW_BACKGROUND_COLOR)
		self.display_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

		# Bind the keypress event to the window
		self.bind('<KeyPress>', lambda event: self.display_frame.process_input(event.char))

class DisplayFrame(tk.Frame):
	"""
	A frame that contains the display area for the calculator's input and result.

	Created by: Anthony Cotales
	Email: ton.cotales@gmail.com
	Version: 1.0.0
	"""

	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)

		# Configure row and column weights for grid layout
		self.rowconfigure(tuple(range(11)), weight=1)
		self.columnconfigure(tuple(range(4)), weight=1)

		# Create an entry widget for the display
		self.display = tk.Entry(self, relief='flat', justify='right', bd=10, font=config.DISPLAY_FONT, fg=config.DISPLAY_FOREGROUND_COLOR)
		self.display.grid(row=0, column=0, columnspan=4, padx=2, pady=12, sticky='nsew')

		# Set the initial display value to '0' and configure the entry widget to be readonly,
		# simulating a typical calculator behavior
		self.display.insert(0, config.DISPLAY_INITIAL_VALUE)
		self.display.configure(state='readonly')

		# Configure the entry widget to validate input on each key press
		self.display.configure(validate='key', validatecommand=(self.register(self.validate_input), '%P'))

		# Create buttons dynamically from the 'buttons' list
		for text, row, column in config.BUTTONS:

			columnspan = 2 if text == '0' else None

			button = tk.Button(self, text=text, relief='groove', cursor='hand2', font=config.BUTTON_FONT)
			button.grid(row=row, column=column, rowspan=2, columnspan=columnspan, sticky='nsew')
			button.configure(command=lambda key=text: self.process_input(key))

	def validate_input(self, new_value):
		"""Validate input to ensure the length doesn't exceed 17 characters."""
		return len(new_value) <= 17 

	def clear_display(self):
		"""Clears the display and resets it to the initial value '0'."""
		self.display.configure(state='normal')
		self.display.delete(0, 'end')
		self.display.insert(0, config.DISPLAY_INITIAL_VALUE)
		self.display.configure(state='readonly')

	def evaluate_expression(self, expression):
		"""
		Evaluates the given mathematical expression and returns the result
		of the evaluated expression, or 'Error' if invalid.
		"""
		try:
			# Replace the calculator symbols with Python's math operators
			expression = expression.translate(str.maketrans(config.OPERATOR_MAP))
			expression_result = eval(expression)

		except (SyntaxError, ZeroDivisionError, Exception):
			# If an error occurs (e.g., invalid syntax), return a generic error message
			return config.DISPLAY_ERROR

		else:
			# If the result is None (invalid expression), set it to 'Error'
			if isinstance(expression_result, type(None)):
				expression_result = config.DISPLAY_ERROR

			# Round the result to 15 decimal places for precision
			result = round(expression_result, ndigits=15)

			# If the result is effectively an integer (i.e., ends with '.0'), convert to int
			if str(result).endswith('.0'):
				result = int(result)

			# Return the result (either as a float or int) casted into a str
			return str(result)

	def process_input(self, input_value):
		"""Processes the input from both button clicks and keyboard presses."""

		## Clear the display when 'C' or ESC key is pressed
		if input_value in ['C', '\x1b']:
			self.clear_display()

		## Handle backspace when '←' or backspace key is pressed
		elif input_value in ['←', '\x08']:

			# Clear display if it shows 'Error'
			if self.display.get() == config.DISPLAY_ERROR:
				self.clear_display()

			# Remove the last character if display value is not '0'
			elif self.display.get() != config.DISPLAY_INITIAL_VALUE:
				self.display.configure(state='normal')
				self.display.delete(len(self.display.get()) - 1, 'end')
				self.display.configure(state='readonly')

				# Reset display to '0' if it becomes empty
				if len(self.display.get()) == 0:
					self.clear_display()

		## Handle percentage ('%')
		elif input_value == '%':
			# Only process if display is not showing 'Error' or initial value '0'
			if self.display.get() not in [config.DISPLAY_ERROR, config.DISPLAY_INITIAL_VALUE]:

				# Split the expression by operators to separate numbers and operators
				base_expression = re.split(r'([+–×÷\-/*])', self.display.get())

				# Case 1: Single number or scientific notation, divide by 100
				if len(base_expression) == 1 or config.SCIENTIFIC_NOTATION in self.display.get():
					display_expression = self.evaluate_expression(self.display.get() + '/100')

				# Case 2: Multiple parts, handle percentage based on operator
				elif len(base_expression) > 1 and config.SCIENTIFIC_NOTATION not in self.display.get():
					operation = base_expression[-2]
					percentage = base_expression[-1]
					value = self.display.get()[0: len(self.display.get()) - (len(percentage) + len(operation))]

					# If operator is * or /, divide percentage by 100
					if operation in ['×', '÷', '*', '/']:
						percentage = self.evaluate_expression(f'{percentage}/100')
					# If operator is + or -, calculate percentage of the value
					elif operation in['+', '–', '-']:
						percentage = self.evaluate_expression(f'{value}*({percentage}/100)')

					# Rebuild the expression with the updated percentage
					display_expression = ''.join(value + operation + percentage)

			else:
				# If the display is in an invalid state ('Error' or '0'), leave the display unchanged
				display_expression = self.display.get()

			# Update display with the calculated percentage result
			self.display.configure(state='normal')
			self.display.delete(0, 'end')
			self.display.insert(0, display_expression)
			self.display.configure(state='readonly')

		## Handle operators, ensure the input value isn't empty or starting with an operator
		elif input_value in config.DISPLAY_OPERATORS + config.PYTHON_OPERATORS:
			operator = '-' if input_value == '–' else input_value

			# Append the operator if the last character in the display is a digit
			if self.display.get()[-1].isdigit():
				self.display.configure(state='normal')
				self.display.insert('end', operator)
				self.display.configure(state='readonly')

	    ## Handle the '=' button or Enter key press to evaluate the expression
		elif input_value in ['=', '\r']:
			# Retrieve the current expression from the display and evaluate it
			result = self.evaluate_expression(self.display.get())

			# Clear the display and show the evaluated result
			self.display.configure(state='normal')
			self.display.delete(0, 'end')
			self.display.insert(0, str(result))
			self.display.configure(state='readonly')

		## Handle decimal point ('.')
		elif input_value == '.':

			if config.SCIENTIFIC_NOTATION not in self.display.get():
				base_expression = re.split(r'([+–×÷\-/*])', self.display.get())

				if base_expression[-1].isdigit():
					self.display.configure(state='normal')
					self.display.insert('end', input_value)
					self.display.configure(state='readonly')

				elif not base_expression[-1]:
					self.display.configure(state='normal')
					self.display.insert('end', config.DISPLAY_INITIAL_VALUE + input_value)
					self.display.configure(state='readonly')

		## Handle digits (0-9)
		elif input_value.isdigit():
			
			if self.display.get() != config.DISPLAY_ERROR:

				if self.display.get() == config.DISPLAY_INITIAL_VALUE:
					self.display.configure(state='normal')
					self.display.delete(0, 'end')
					self.display.configure(state='readonly')

				self.display.configure(state='normal')
				self.display.insert('end', input_value)
				self.display.configure(state='readonly')

		## In case of odd occurence disable editing of the display
		self.display.configure(state='readonly')


if __name__ == "__main__":
	# Create the calculator instance and run the application
	app = Calculator()
	app.mainloop()