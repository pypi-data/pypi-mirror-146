import tkinter as tk
from tkinter import ttk

from app import App

root = tk.Tk()
root.title("Portscanner")
root.configure(padx=5, pady=5)

style = ttk.Style()
style.theme_use('clam')

app = App(root)

root.mainloop()