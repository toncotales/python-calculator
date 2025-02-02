import config
import functools
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
			button.configure(command=functools.partial(self.process_input, text))

	def validate_input(self, new_value):
		"""Validate input to ensure the length doesn't exceed 17 characters."""
		return len(new_value) <= 17 

	def clear_display(self):
		"""Clears the display and resets it to the initial value '0'."""
		self.display.delete(0, 'end')
		self.display.insert(0, config.DISPLAY_INITIAL_VALUE)

	def process_input(self, input_value):
		"""Processes the input from both button clicks and keyboard presses."""
		pass




if __name__ == "__main__":
	# Create the calculator instance and run the application
	app = Calculator()
	app.mainloop()
