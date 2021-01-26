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

class Table:
	def __init__(self, root, start_row, data):
		self.start_row = start_row
		self.root = root
		self.update_table(data)

	def update_table(self, data):
		self.data = data

		if len(self.data) == 0:
			return

		self.rows = get_rows(data)
		self.columns = get_columns(data)

		self.e = tk.Label(self.root, text="ID", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=0)
		self.e = tk.Label(self.root, text="Date", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=1)
		self.e = tk.Label(self.root, text="Name", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=2)
		self.e = tk.Label(self.root, text="Description", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=3)
		self.e = tk.Label(self.root, text="Language", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=4)

		for i in range(self.rows):
			for j in range(self.columns):
				self.e = tk.Entry(self.root, width=20, fg=color_fg, bg=color_bg)
				self.e.grid(row=1 + self.start_row + i, column=j)
				self.e.insert(tk.END, self.data[i][j])

	def get_final_row():
		return start_row + get_rows(self.rows)

class MainApplication(tk.Frame):
	def __init__(self, master):
		self.master = master
		tk.Frame.__init__(self, self.master)
		self.configure_gui()
		self.create_widgets()

	def configure_gui(self):
		self.master.configure(background="white")
		self.master.title("ural")
		self.master.geometry("800x800")
		self.master.minsize(width=800, height=800)
		self.master.style = ttk.Style()
		self.master.style.theme_use("clam")

	def create_widgets(self):
		labelPName = tk.Label(self.master, text="Project name:", fg=color_fg, bg=color_bg)
		labelPDesc = tk.Label(self.master, text="Description:", fg=color_fg, bg=color_bg)
		labelPLang = tk.Label(self.master, text="Language:", fg=color_fg, bg=color_bg)
		self.entryPName = tk.Entry(self.master, bg=color_bg)
		self.entryPDesc = tk.Entry(self.master, bg=color_bg)
		self.entryPLang = tk.Entry(self.master, bg=color_bg)

		labelPName.grid(row=0, column=0)
		labelPDesc.grid(row=1, column=0)
		labelPLang.grid(row=2, column=0)
		self.entryPName.grid(row=0, column=1)
		self.entryPDesc.grid(row=1, column=1)
		self.entryPLang.grid(row=2, column=1)

		buttonClear = tk.Button(self.master, text="Clear", fg=color_fg, bg=color_bg, command=self.clear)
		buttonSubmit = tk.Button(self.master, text="Submit", fg=color_fg, bg=color_bg, command=self.submit)
		buttonExit = tk.Button(self.master, text="Exit", fg=color_fg, bg=color_bg, command=exit)
		buttonClear.grid(row=3, column=0)
		buttonSubmit.grid(row=3, column=1)
		buttonExit.grid(row=3, column=2)

		self.table = Table(self.master, 4, projects)

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
