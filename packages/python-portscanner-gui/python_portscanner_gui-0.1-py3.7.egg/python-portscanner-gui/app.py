from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import askquestion
from tkinter.filedialog import asksaveasfile 
from portscan import Portscan
from results import Results
from options import OptionsDialog

class App:
	def __init__(self, root):
		self.root = root
		self.scanType = tk.StringVar()
		self.scanner = None
		
		self.defaults = {
			'timeout': 5,
			'threads': 10,
			'retries': 3
		}
		
		menubar = Menu(root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Options", command=self.options)
		filemenu.add_command(label="Reset", command=self.reset)
		filemenu.add_command(label="Save", command=self.save)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="Menu", menu=filemenu)
		
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About...", command=self.about)
		menubar.add_cascade(label="Help", menu=helpmenu)
		
		root.config(menu=menubar)
		
		self.topFrame = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
		self.topFrame.grid(column=0, row=0, padx=5, pady=5)
		
		self.infoFrame = ttk.Frame(self.topFrame, borderwidth=1)
		sepf.infoFrame.grid(column=0, row=0)
		self.targetLabel = ttk.Label(self.infoFrame, text="Enter target domain(s) or IP(s), separated by commas.")
		self.targetLabel.grid(column=0, row=0, pady=5)
		self.targetInput = ttk.Entry(self.infoFrame)
		self.targetInput.grid(column=1, row=0, padx=5, pady=5)
		self.portLabel = ttk.Label(self.infoFrame, text="Ports to scan. Can be 'basic', 'all', or any comma-separated list.")
		self.portLabel.grid(column=0, row=1)
		self.portInput = ttk.Entry(self.infoFrame)
		self.portInput.grid(column=1, row=1, padx=5, pady=5)
		
		self.checkFrame = ttk.Frame(self.topFrame, relief=tk.RAISED, borderwidth=1)
		self.checkFrame.grid(column=0, row=1, padx=5, pady=5)
		
		checkLabel = ttk.Label(self.checkFrame, text="Type of scan")
		checkLabel.grid(column=0, row=0, pady=5)
		
		ttk.Radiobutton(self.checkFrame, text='TCP', variable=self.scanType, value='tcp').grid(row=1, column=0)
		ttk.Radiobutton(self.checkFrame, text='UDP', variable=self.scanType, value='udp').grid(row=1, column=1)
		ttk.Radiobutton(self.checkFrame, text='ACK', variable=self.scanType, value='ack').grid(row=1, column=2)
		ttk.Radiobutton(self.checkFrame, text='FIN', variable=self.scanType, value='fin').grid(row=1, column=3)
		ttk.Radiobutton(self.checkFrame, text='SYN', variable=self.scanType, value='syn').grid(row=1, column=4)
		ttk.Radiobutton(self.checkFrame, text='NULL', variable=self.scanType, value='null').grid(row=1, column=5)
		ttk.Radiobutton(self.checkFrame, text='XMAS', variable=self.scanType, value='xmas').grid(row=1, column=6)
		
		submitButton = ttk.Button(self.topFrame, text="Scan", command=self.click).grid(column=0, row=2)
		
		self.resultsFrame = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
		self.resultsFrame.grid(column=0, row=1, padx=5, pady=5)
		self.resFrame = Results(self.resultsFrame)
	
	def updateDefaults(self, map):
		for key, value in map.items():
			self.defaults[key] = value
	
	def save(self):
		txt = self.resFrame.resultsBox.get()
		if txt != '':
			files = [('All Files', '*.*'), ('Text Document', '*.txt'), ('LOG File', '*.log')]
			filePath = asksaveasfile(filetypes = files, defaultextension = files, initialfile = "output.txt")
			f = open(filePath,'w')
			f.write(txt)
			f.close()
	
	def reset(self):
		response = askquestion("Reset?", "Reset all data?", icon='warning')
		if response == "yes":
			self.resFrame.resultsBox.delete(0, tk.END)
	
	def about(self):
		txt = "Port Scanner by Jason O'Neal\r\nPlease use responsibly."
		messagebox.showinfo("About...", txt)
	
	def options(self):
		self.dialog = OptionsDialog(self)
	
	def click(self):
		targetData = self.targetInput.get()
		portData = self.portInput.get()
		
		try:
			self.scanner = Portscan(self.scanType, targetData, portData, self.resFrame)
			self.scanner.start()
		except KeyboardInterrupt:
			print("\n\n")
			print('Program halted by user')
			print('Shutting down.')
			exit(1)