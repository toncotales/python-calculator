import tkinter as tk
from tkinter import PhotoImage

from config import *


class CalculatorApp(tk.Tk):
	def __init__(self):
		super().__init__()

		# Setting window configurations.
		self.title(WINDOW_TITLE)
		self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
		self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.iconphoto(False, PhotoImage(data=WINDOW_ICON))

		# Create the main frame for the calculator widgets.
		self.widget_frame = WidgetFrame(self, bg=WINDOW_BACKGROUND_COLOR)
		self.widget_frame.place(x=0, y=0, relwidth=1, relheight=1)

		# Bind the keypress event to the window.
		self.bind('<KeyPress>', lambda event: self.widget_frame.process_input(event.char))


class WidgetFrame(tk.Frame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)

		# Top frame containing the display of the calculator.
		top_container = tk.Frame(self)
		top_container.place(relx=0.04, rely=0.05, relwidth=0.92, relheight=0.2)

		# Bottom frame containing the buttons of the calculator.
		bottom_container = tk.Frame(self)
		bottom_container.place(relx=0.04, rely=0.29, relwidth=0.92, relheight=0.67)

		# Configure bottom frame for a grid layout.
		bottom_container.rowconfigure(tuple(range(5)), weight=1, uniform='a')
		bottom_container.columnconfigure(tuple(range(4)), weight=1, uniform='a')

		# Create the display with a tk.Entry widget.
		self.display = tk.Entry(top_container, relief='flat', justify='right', bd=10, font=DISPLAY_FONT, fg=DISPLAY_FOREGROUND_COLOR)
		self.display.place(x=0, y=0, relwidth=1, relheight=1)
		
		# Set initial display value to '0' and configure entry widget to be readonly,
		# simulating a typical calculator behavior and adding a validate command to
		# validate input to set a certain length of the display on each key press.
		self.display.insert(0, DISPLAY_INITIAL_VALUE)
		self.display.configure(state='readonly')
		self.display.configure(validate='key', validatecommand=(self.register(self.validate_input), '%P'))

		# Create the buttons.
		for text, row, column in BUTTONS2:
			columnspan = 2 if text == '0' else None
			button = tk.Button(bottom_container, text=text, relief='groove', cursor='hand2', font=BUTTON_FONT)
			button.grid(row=row, column=column, columnspan=columnspan, sticky='nsew')
			button.configure(command=lambda key=text: self.process_input(key))

	def validate_input(self, display_value):
		"""Validate input to ensure the length doesn't exceed 17 characters."""
		return len(display_value) <= 17

	def process_input(self, input_value):
		"""Processes the input from both button clicks and keyborad presses."""
		# Clear the display when 'C' or ESC key is pressed
		if input_value in ['C', '\x1b']:
			self.clear_display()

		# Handle backspace when '←' or backspace key is pressed
		elif input_value in ['←', '\x08']:
			self.display_delete_handler()

		# Handle percentage ('%')
		elif input_value == '%':
			self.display_percentage_handler()

		# Handle math operators
		elif input_value in DISPLAY_OPERATORS + PYTHON_OPERATORS:
			self.display_operator(input_value)

		# Handle decimal point ('.')
		elif input_value == '.':
			self.display_decimal_point()

		# Handle digits or numbers
		elif input_value.isdigit():
			self.display_number(input_value)

	    # Handle the '=' button or Enter key press to evaluate the expression
		elif input_value in ['=', '\r']:
			self.display_equalsign()

		# In case of odd occurance, disable editing of the display
		self.display.configure(state='readonly')

	def clear_display(self):
		"""Clears the display and resets it to the initial value '0'."""
		self.display.configure(state='normal')
		self.display.delete(0, 'end')
		self.display.insert(0, DISPLAY_INITIAL_VALUE)
		self.display.configure(state='readonly')

	def display_delete_handler(self):
		"""Deletes a single character in the display."""
		# Clear display if it shows 'Error'
		if self.display.get() == DISPLAY_ERROR:
			self.clear_display()
		# Remove the last character if display value is not '0'
		elif self.display.get() != DISPLAY_INITIAL_VALUE:
			self.display.configure(state='normal')
			self.display.delete(len(self.display.get()) - 1, 'end')
			self.display.configure(state='readonly')

			# Reset display to '0' if it becomes empty
			if not len(self.display.get()):
				self.clear_display()

	def display_operator(self, operator):
		"""Insert math operator to the display."""
		operator = '-' if operator == '–' else operator
		# Append the operator if the last character in the display is a digit
		if self.display.get()[-1].isdigit():
			self.display.configure(state='normal')
			self.display.insert('end', operator)
			self.display.configure(state='readonly')

	def display_number(self, number):
		"""Insert number to the display."""
		if self.display.get() != DISPLAY_ERROR:

			if self.display.get() == DISPLAY_INITIAL_VALUE:
				self.display.configure(state='normal')
				self.display.delete(0, 'end')
				self.display.configure(state='readonly')

			self.display.configure(state='normal')
			self.display.insert('end', number)
			self.display.configure(state='readonly')

	def display_decimal_point(self):
		"""Handle decimal point function."""
		if SCIENTIFIC_NOTATION not in self.display.get():
			# Split the expression by operators to separate numbers and operators.
			expressions = get_base_expression(self.display.get())

			if expressions[-1].isdigit():
				self.display.configure(state='normal')
				self.display.insert('end', '.')
				self.display.configure(state='readonly')

			elif not expressions[-1]:
				self.display.configure(state='normal')
				self.display.insert('end', f'{DISPLAY_INITIAL_VALUE}.')
				self.display.configure(state='readonly')

	def display_percentage_handler(self):
		"""Handle percentage insert operations to the display."""
		# Process only if display is not 'Error' or '0'
		if self.display.get() not in [DISPLAY_ERROR, DISPLAY_INITIAL_VALUE]:
			expressions = get_base_expression(self.display.get())
			print(expressions)

			# Case 1: Single number or scientific notation, divide by 100
			if len(expressions) == 1 or SCIENTIFIC_NOTATION in self.display.get():
				display_expression = evaluate_expression(f'{self.display.get()}/100')

			# Case 2: Multiple parts, handle percentage based on operator
			elif len(expressions) > 1 and SCIENTIFIC_NOTATION not in self.display.get():
				operator, percentage = expressions[-2], expressions[-1]
				value_index = len(self.display.get()) - (len(percentage) + len(operator))
				value = self.display.get()[0:value_index]

				# If operator is * or /, divide percentage by 100
				if operator in ['×', '÷', '*', '/']:
					percentage = evaluate_expression(f'{percentage}/100')
				# If operator is + or -, calculate percentage of the value
				elif operator in ['+', '–', '-']:
					percentage = evaluate_expression(f'{value}*({percentage}/100)')

				# Rebuild the expression with the updated percentage
				display_expression = ''.join(value + operator + percentage)

			# Case 3: Multiple parts but there is a scientific notation
			elif len(expressions) > 1 and SCIENTIFIC_NOTATION in self.display.get():
				print('YAWA')
		else:
			# Leave the display unchanged
			display_expression = self.display.get()

		# print(f'display expression: {display_expression}')
		# Update display with the calculated percentage result
		self.display.configure(state='normal')
		self.display.delete(0, 'end')
		self.display.insert(0, display_expression)
		self.display.configure(state='readonly')

	def display_equalsign(self):
		"""Processes the display values as math expressions."""
		if self.display.get() == DISPLAY_ERROR:
			self.clear_display()
		else:
			result = evaluate_expression(self.display.get())
			if result != self.display.get():
				self.display.configure(state='normal')
				self.display.delete(0, 'end')
				self.display.insert(0, result)
				self.display.configure(state='readonly')


if __name__ == '__main__':
	app = CalculatorApp()
	app.mainloop()
