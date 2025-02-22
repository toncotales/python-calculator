import tkinter as tk
from tkinter import PhotoImage
from config import *



class Calculator(tk.Tk):
	def __init__(self):
		super().__init__()

		# Setting window configurations.
		self.title(WINDOW_TITLE)
		self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
		self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.iconphoto(False, PhotoImage(data=WINDOW_ICON))

		# Create the main frame for the calculator widgets.
		self.calc = WidgetFrame(self, bg=WINDOW_BACKGROUND_COLOR)
		self.calc.place(x=0, y=0, relwidth=1, relheight=1)

		# Bind the keypress event to the window.
		self.bind('<KeyPress>', lambda event: self.calc.process_insert(event.char))

	def open(self):
		"""Start the GUI event loop."""
		self.mainloop()

	def close(self):
		"""Close the calculator window."""
		self.destroy()


class WidgetFrame(tk.Frame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)

		# Top frame containing the display of the calculator.
		top_container = tk.Frame(self, bd=5, bg=FRAME_BORDER_COLOR)
		top_container.place(relx=0.04, rely=0.05, relwidth=0.92, relheight=0.2)

		# Bottom frame containing the buttons of the calculator.
		bottom_container = tk.Frame(self, relief='flat', bd=5, bg=FRAME_BORDER_COLOR)
		bottom_container.place(relx=0.04, rely=0.29, relwidth=0.92, relheight=0.67)

		# Configure bottom frame for a grid layout.
		bottom_container.rowconfigure(tuple(range(5)), weight=1, uniform='a')
		bottom_container.columnconfigure(tuple(range(4)), weight=1, uniform='a')

		# Create the display with a tk.Entry inside a tk.Frame widget.
		border_frame = tk.Frame(top_container, relief='groove', bd=1)
		border_frame.place(relwidth=1, relheight=1)

		self.display = tk.Entry(border_frame, relief='flat', justify='right', bd=10, font=DISPLAY_FONT, fg=DISPLAY_FOREGROUND_COLOR)
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
		if key in ['C', '\x1b']:  # When key press 'C' or ESC
			self.clear_display()

		if key in ['←', '\x08']:  # When key press '←' or backspace
			self.delete_handler()

		if key == '%':  # When key press '%'
			self.percentage_handler()

		if key in OPERATORS:  # When math operators
			self.insert_operator(key)

		if key == '.':  # When key press '.'
			self.insert_decimal()

		if key.isdigit():  # When key press is a digit
			self.insert_number(key)
	    
		if key in ['=', '\r']:  # When key press '='
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
			expressions = split_expression(self.display.get())
		else:
			expressions = split_expression_with_exponents(self.display.get())

		if expressions[-1].isdigit():
			self.display.configure(state='normal')
			self.display.insert('end', '.')
			self.display.configure(state='readonly')

		if not expressions[-1] or expressions[-1] in OPERATORS:
			self.display.configure(state='normal')
			self.display.insert('end', '0.')
			self.display.configure(state='readonly')

	def percentage_handler(self):
		# Handle the percentage functionality
		if self.display.get() not in [ERROR, INITIAL_VALUE]:
			if SCIENTIFIC_NOTATION not in self.display.get():
				expressions = split_expression(self.display.get())
			else:
				expressions = split_expression_with_exponents(self.display.get())
			
			if not expressions[0]:
				negative = ''.join(expressions[:3])
				values = [i for i in expressions[4:]]
				expressions = [negative] + values
			
			# print(f'Expressions: {expressions}')

			if len(expressions) == 1:
				if expressions[0].isdigit() or not expressions[0].endswith('.'):
					# print(f'[OK] -> {expressions[0]}/100')
					test_result = evaluate_expression(f'{expressions[0]}/100')

					self.display.configure(state='normal')
					self.display.delete(0, 'end')
					self.display.insert(0, test_result)
					self.display.configure(state='readonly')

			else:
				if expressions[-1]:
					if expressions[-1].isdigit() or not expressions[-1].endswith('.'):
						# print(f'[OK] -> {expressions}')
						base = expressions[:-1]
						operation_identifier = expressions[-2]
						percentage_value = expressions[-1]

						if operation_identifier in ['×', '÷', '*', '/']:
							base_result = evaluate_expression(''.join(expressions[:-2]))
							percentage_value = evaluate_expression(f'{percentage_value}/100')
							base = [str(base_result), operation_identifier]


						if operation_identifier in ['+', '–', '-']:
							base_result = evaluate_expression(''.join(expressions[:-2]))
							percentage = evaluate_expression(f'{percentage_value}/100')
							percentage_value = evaluate_expression(f'{base_result}*{percentage}')

						new_display = ''.join(base) + str(percentage_value)

						if ERROR not in new_display:
							# print(f'[DISPLAY] -> {new_display}')
							self.display.configure(state='normal')
							self.display.delete(0, 'end')
							self.display.insert(0, new_display)
							self.display.configure(state='readonly')


if __name__ == '__main__':

	app = Calculator()
	app.open()