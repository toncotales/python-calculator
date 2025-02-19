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

		# Top frame containing the display widget of the calculator.
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


	def validate_input(self, display_value):
		"""Validate input to ensure the length doesn't exceed 17 characters."""
		return len(display_value) <= 17

	def process_input(self, input_value):
		"""Processes the input from both button clicks and keyborad presses."""
		pass




if __name__ == '__main__':
	app = CalculatorApp()
	app.mainloop()
