import tkinter as tk
import config


class Calculator(tk.Tk):
	"""
	A simple and user-friendly calculator built using Python and Tkinter.

	Created by: Anthony Cotales
	Email: ton.cotales@gmail.com
	Version: 1.0.0
	"""

	def __init__(self):
		super().__init__()

		self.title(config.WINDOW_TITLE)
		self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}')
		self.minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
		self.maxsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)


if __name__ == "__main__":
	# Create the calculator instance and run the application
	app = Calculator()
	app.mainloop()
