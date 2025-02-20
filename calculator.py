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
		self.display.insert(0, INITIAL_VALUE)
		self.display.configure(state='readonly')
		self.display.configure(validate='key', validatecommand=(self.register(length_validator), '%P'))

		# Create the buttons.
		for text, row, column in BUTTONS:
			columnspan = 2 if text == '0' else None
			button = tk.Button(bottom_container, text=text, relief='groove', cursor='hand2', font=BUTTON_FONT)
			button.grid(row=row, column=column, columnspan=columnspan, sticky='nsew')
			button.configure(command=lambda key=text: self.process_insert(key))

	def process_insert(self, key):
		"""
		Processes the input from both button clicks and keyborad presses.
		"""
		if key in ['C', '\x1b']:  # When 'C' or ESC key is pressed
			self.clear_display()

		if key in ['←', '\x08']:  # When '←' or backspace key is pressed
			self.delete_handler()

		if key == '%':  # When '%' is pressed
			self.percentage_handler()

		if key in OPERATORS:  # When math operators
			self.insert_operator(key)

		if key == '.':  # When '.' or decimal point is pressed
			self.insert_decimal()

		if key.isdigit():  # When a number is pressed
			self.insert_number(key)
	    
		if key in ['=', '\r']:  # When '=' is pressed
			self.equalsign_handler()

		# In case of odd occurance, disable editing of the display
		self.display.configure(state='readonly')

	def clear_display(self):
		# Clear the display and reset value to zero
		self.display.configure(state='normal')
		self.display.delete(0, 'end')
		self.display.insert(0, INITIAL_VALUE)
		self.display.configure(state='readonly')

	def delete_handler(self):
		# Delete single character in the display
		if self.display.get() not in [ERROR, INITIAL_VALUE]:

			self.display.configure(state='normal')
			self.display.delete(len(self.display.get()) - 1, 'end')
			self.display.configure(state='readonly')

			# Reset to zero if display becomes empty
			if not len(self.display.get()):
				self.clear_display()
		else:
			self.clear_display()

	def insert_number(self, number):
		# Inserting a number to the display
		if self.display.get() != ERROR:

			if self.display.get() == INITIAL_VALUE:
				self.display.configure(state='normal')
				self.display.delete(0, 'end')
				self.display.configure(state='readonly')

			self.display.configure(state='normal')
			self.display.insert('end', number)
			self.display.configure(state='readonly')

	def insert_operator(self, operator):
		# Inserting a math operator to the display
		operator = '-' if operator == '–' else operator
		# Append the operator if the last character in the display is a digit
		if self.display.get()[-1].isdigit():
			self.display.configure(state='normal')
			self.display.insert('end', operator)
			self.display.configure(state='readonly')

	def equalsign_handler(self):
		# Evaluate the expression and display the result
		if self.display.get() in [ERROR, INITIAL_VALUE]:
			self.clear_display()
		else:
			result = evaluate_expression(self.display.get())
			if result != self.display.get():
				self.display.configure(state='normal')
				self.display.delete(0, 'end')
				self.display.insert(0, result)
				self.display.configure(state='readonly')

	def insert_decimal(self):
		# Inserting a decimal point in the display
		if SCIENTIFIC_NOTATION not in self.display.get():
			# Split the numbers and operators.
			expressions = split_expression(self.display.get())

			if expressions[-1].isdigit():
				self.display.configure(state='normal')
				self.display.insert('end', '.')
				self.display.configure(state='readonly')

			elif not expressions[-1]:
				self.display.configure(state='normal')
				self.display.insert('end', '0.')
				self.display.configure(state='readonly')

	def percentage_handler(self):
		# TODO: Need to refactor the logic on this functionality
		pass
		# """Handle percentage insert operations to the display."""
		# # Process only if display is not 'Error' or '0'
		# if self.display.get() not in [ERROR, INITIAL_VALUE]:
		# 	expressions = split_expression(self.display.get())
		# 	print(expressions)

		# 	# Case 1: Single number or scientific notation, divide by 100
		# 	if len(expressions) == 1 or SCIENTIFIC_NOTATION in self.display.get():
		# 		display_expression = evaluate_expression(f'{self.display.get()}/100')

		# 	# Case 2: Multiple parts, handle percentage based on operator
		# 	elif len(expressions) > 1 and SCIENTIFIC_NOTATION not in self.display.get():
		# 		operator, percentage = expressions[-2], expressions[-1]
		# 		value_index = len(self.display.get()) - (len(percentage) + len(operator))
		# 		value = self.display.get()[0:value_index]

		# 		# If operator is * or /, divide percentage by 100
		# 		if operator in ['×', '÷', '*', '/']:
		# 			percentage = evaluate_expression(f'{percentage}/100')
		# 		# If operator is + or -, calculate percentage of the value
		# 		elif operator in ['+', '–', '-']:
		# 			percentage = evaluate_expression(f'{value}*({percentage}/100)')

		# 		# Rebuild the expression with the updated percentage
		# 		display_expression = ''.join(value + operator + percentage)

		# 	# Case 3: Multiple parts but there is a scientific notation
		# 	elif len(expressions) > 1 and SCIENTIFIC_NOTATION in self.display.get():
		# 		print('YAWA')
		# else:
		# 	# Leave the display unchanged
		# 	display_expression = self.display.get()

		# # print(f'display expression: {display_expression}')
		# # Update display with the calculated percentage result
		# self.display.configure(state='normal')
		# self.display.delete(0, 'end')
		# self.display.insert(0, display_expression)
		# self.display.configure(state='readonly')




if __name__ == '__main__':
	app = CalculatorApp()
	app.mainloop()
