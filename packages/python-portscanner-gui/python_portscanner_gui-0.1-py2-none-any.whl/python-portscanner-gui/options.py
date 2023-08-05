import tkinter as tk
from tkinter import ttk

class OptionsDialog:
	def __init__(self, app):
		self.app = app
		self.popup = tk.Toplevel(app.root)
		
		self.label = ttk.Label(self.popup, text="Options")
		self.label.grid(row=0, column=0)
		
		self.frame = ttk.Frame(self.popup, relief=tk.RAISED, borderwidth=1)
		self.frame.grid(column=0, row=1, padx=5, pady=5)
		
		self.timeoutLabel = ttk.Label(self.frame, text="Timeout (in seconds)")
		self.timeoutLabel.grid(column=0, row=0, pady=5)
		self.timeoutInput = ttk.Entry(self.frame)
		self.timeoutInput.grid(column=1, row=0, padx=5, pady=5)
		self.timeoutInput.insert(0, self.app.defaults.timeout)
		
		self.threadsLabel = ttk.Label(self.frame, text="Number of threads")
		self.threadsLabel.grid(column=0, row=1, pady=5)
		self.threadsInput = ttk.Entry(self.frame)
		self.threadsInput.grid(column=1, row=1, padx=5, pady=5)
		self.threadsInput.insert(0, self.app.defaults.threads)
		
		self.retriesLabel = ttk.Label(self.frame, text="Number of retries")
		self.retriesLabel.grid(column=0, row=2, pady=5)
		self.retriesInput = ttk.Entry(self.frame)
		self.retriesInput.grid(column=1, row=2, padx=5, pady=5)
		self.retriesInput.insert(0, self.app.defaults.retries)
		
		self.submit = ttk.Button(self.popup, text="Save", command=self.click).grid(column=0, row=2)
	
	def click(self):
		dictionary = {
			'timeout': self.timeoutInput.get(),
			'threads': self.threadsInput.get(),
			'retries': self.retriesInput.get()
		}
		
		self.app.updateDefaults(dictionary)
		self.popup.destroy()