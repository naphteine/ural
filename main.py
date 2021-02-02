import tkinter as tk
from tkinter import messagebox as tkmsgbox
from tkinter import ttk as ttk
from datetime import datetime as dtime
import sqlite3 as sq3

# Global variables
tasks_list = []
color_bg = "white"
color_fg = "black"
projects = []

def get_rows(data):
	return len(data)

def get_columns(data):
	return len(data[0])

def check_int(s):
	if s[0] in ('-', '+'):
		return s[1:].isdigit()
	return s.isdigit()

class Table:
	def __init__(self, root, data):
		self.root = root
		self.update_table(data)

	def update_table(self, data):
		# Setup data
		self.data = data

		if len(self.data) == 0:
			return

		self.rows = get_rows(data)
		self.columns = get_columns(data)

		# Setup Treeview
		self.tree = ttk.Treeview(self.root, selectmode='browse')
		self.tree.grid(row=0, column=0, sticky='we')
		self.tree['show'] = 'headings'

		# Treeview: Columns setup
		self.tree['columns'] = ["1", "2", "3", "4", "5"]

		self.tree.column("1", width=50, anchor='c')
		self.tree.column("2", width=150, anchor='w')
		self.tree.column("3", width=100, anchor='w')
		self.tree.column("4", width=300, anchor='w')
		self.tree.column("5", width=100, anchor='w')

		self.tree.heading("1", text="ID", command=lambda: \
						  self.treeview_sort_column(self.tree, 1, "ID", False))
		self.tree.heading("2", text="Date", command=lambda: \
						  self.treeview_sort_column(self.tree, 2, "Date", False))
		self.tree.heading("3", text="Name", command=lambda: \
						  self.treeview_sort_column(self.tree, 3, "Name", False))
		self.tree.heading("4", text="Description", command=lambda: \
						  self.treeview_sort_column(self.tree, 4, "Description", False))
		self.tree.heading("5", text="Language", command=lambda: \
						  self.treeview_sort_column(self.tree, 5, "Language", False))

		# Treeview: Insert data
		for i in range(self.rows):
			self.tree.insert("", 'end', text=i, values=(self.data[i][0],
			self.data[i][1],self.data[i][2],self.data[i][3],self.data[i][4]))

		# Vertical scrollbar
		self.vsbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
		self.vsbar.grid(row=0, column=1, sticky='ns')
		self.tree.configure(yscrollcommand=self.vsbar.set)

	def treeview_sort_column(self, tv, col, text, reverse):
		list = [(tv.set(k, col), k) for k in tv.get_children('')]
		list.sort(reverse=reverse)

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(list):
			tv.move(k, '', index)

		# reverse sort next time
		tv.heading(col, text=text, command=lambda _col=col, _text=text: \
				   self.treeview_sort_column(tv, _col, _text, not reverse))

class MainApplication(tk.Frame):
	def __init__(self, master):
		self.master = master
		tk.Frame.__init__(self, self.master)
		self.configure_gui()
		self.create_widgets()

	def configure_gui(self):
		self.grid()
		self.master.configure(background="white")
		self.master.title("ural")
		self.master.geometry("1200x600")
		self.master.minsize(width=1200, height=600)
		self.master.resizable(width=0, height=0)
		self.master.style = ttk.Style()
		self.master.style.theme_use("clam")

		for row in range(6):
			self.master.rowconfigure(row, weight=1)

		for column in range(5):
			self.master.columnconfigure(column, weight=1)

		self.frame1 = tk.Frame(self.master, bg="white")
		self.frame1.grid(row = 0, column = 0, rowspan = 2, columnspan = 5, sticky = "wens")
		self.frame2 = tk.Frame(self.master, bg="white")
		self.frame2.grid(row = 2, column = 0, rowspan = 4, columnspan = 5, sticky = "wens")

	def create_widgets(self):
		labelPName = tk.Label(self.frame1, text="Project name:", fg=color_fg, bg=color_bg)
		labelPDesc = tk.Label(self.frame1, text="Description:", fg=color_fg, bg=color_bg)
		labelPLang = tk.Label(self.frame1, text="Language:", fg=color_fg, bg=color_bg)
		self.entryPName = tk.Entry(self.frame1, bg=color_bg)
		self.entryPDesc = tk.Entry(self.frame1, bg=color_bg)
		self.entryPLang = tk.Entry(self.frame1, bg=color_bg)

		labelPName.grid(row=0, column=0)
		labelPDesc.grid(row=1, column=0)
		labelPLang.grid(row=2, column=0)
		self.entryPName.grid(row=0, column=1)
		self.entryPDesc.grid(row=1, column=1)
		self.entryPLang.grid(row=2, column=1)

		buttonClear = tk.Button(self.frame1, text="Clear", fg=color_fg, bg=color_bg, command=self.clear)
		buttonSubmit = tk.Button(self.frame1, text="Submit", fg=color_fg, bg=color_bg, command=self.submit)
		buttonExit = tk.Button(self.frame1, text="Exit", fg=color_fg, bg=color_bg, command=exit)
		buttonClear.grid(row=3, column=0)
		buttonSubmit.grid(row=3, column=1)
		buttonExit.grid(row=3, column=2)

		self.table = Table(self.frame2, projects)

	def submit(self):
		global projects

		if self.entryPName.get() == "" or self.entryPDesc.get() == "" or self.entryPLang.get() == "":
			tkmsgbox.showerror("Input error!")
			return

		count = 0

		if len(projects) != 0:
			count = get_rows(projects)

		data = [count,
				dtime.now().strftime("%Y-%m-%d %H:%M:%S"),
				self.entryPName.get(),
				self.entryPDesc.get(),
				self.entryPLang.get()
		]

		if len(projects) != 0:
			projects.append(data)
		else:
			projects = [data]

		# Also add data into DB
		conn = sq3.connect('ural.db')
		c = conn.cursor()
		c.execute(
			"INSERT INTO projects VALUES (?, ?, ?, ?, ?)",
			(data[0], data[1], data[2], data[3], data[4])
		)
		conn.commit()
		conn.close()

		self.table.update_table(projects)
		self.clear()

	def clear(self):
		self.entryPName.delete(0, tk.END)
		self.entryPDesc.delete(0, tk.END)
		self.entryPLang.delete(0, tk.END)

if __name__ == '__main__':
	# Open DB connection and create table if not exists
	conn = sq3.connect('ural.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS projects
				 (id INTEGER, date TEXT, name TEXT, description TEXT, language TEXT)''')

	# Reading database into global variable
	data = c.execute('SELECT id, date, name, description, language FROM projects').fetchall()

	for row in data:
		projects.append(row)

	conn.close()

	# Start Tkinter and mainloop
	root = tk.Tk()
	main_app = MainApplication(root)
	root.mainloop()
