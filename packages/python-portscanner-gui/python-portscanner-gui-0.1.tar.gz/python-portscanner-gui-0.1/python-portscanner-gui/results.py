from tkinter import *
from tkinter import ttk
import tkinter as tk

class Results:
	def __init__(self, root):
		self.label = ttk.Label(master=root, text="Results")
		self.label.grid(column=0, row=0, padx=10, pady=10)
		
		self.resultsBox = Text(width=49, height=5, bg="white", foreground="black", wrap="word")
		tex_scroll = Scrollbar(orient=VERTICAL)
		tex_scroll.config(command=self.resultsBox.yview)
		self.resultsBox["yscrollcommand"] = tex_scroll.set
		self.resultsBox.grid(column=1, row=4, columnspan=2, sticky="w")
		tex_scroll.grid(column=2, row=4, sticky="nse") 
	
	def display(self, output):
		self.resultsBox.insert(tk.END, output+"\r\n")