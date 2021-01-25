from tkinter import *
from tkinter import messagebox

# Global variables
tasks_list = []
counter = 1

# Theme
color_bg = "white"
color_fg = "black"

projects = [("ural", "Project manager", "Python3")]

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
		self.rows = get_rows(data)
		self.columns = get_columns(data)

		self.e = Label(gui, text="Name", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=0)
		self.e = Label(gui, text="Description", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=1)
		self.e = Label(gui, text="Language", fg=color_fg, bg=color_bg)
		self.e.grid(row=self.start_row, column=2)

		for i in range(self.rows):
			for j in range(self.columns):
				self.e = Entry(self.root, width=20, fg=color_fg, bg=color_bg)
				self.e.grid(row=1 + self.start_row + i, column=j)
				self.e.insert(END, self.data[i][j])

	def get_final_row():
		return start_row + get_rows(self.rows)

def clear():
	entryPName.delete(0, END)
	entryPDesc.delete(0, END)
	entryPLang.delete(0, END)

def submit():
	global counter

	if entryPName.get() == "" or entryPDesc.get() == "" or entryPLang.get() == "":
		messagebox.showerror("Input error!")
		return

	data = [entryPName.get(), entryPDesc.get(), entryPLang.get()]
	projects.append(data)
	table.update_table(projects)
	clear()

if __name__ == "__main__":
	gui = Tk()
	gui.configure(background="white")
	gui.title("ural")
	gui.geometry("800x800")
	gui.minsize(width=800, height=800)

	labelPName = Label(gui, text="Project name: ", fg=color_fg, bg=color_bg)
	labelPDesc = Label(gui, text="Description: ", fg=color_fg, bg=color_bg)
	labelPLang = Label(gui, text="Language: ", fg=color_fg, bg=color_bg)
	entryPName = Entry(gui, bg=color_bg)
	entryPDesc = Entry(gui, bg=color_bg)
	entryPLang = Entry(gui, bg=color_bg)

	labelPName.grid(row=0, column=0)
	labelPDesc.grid(row=1, column=0)
	labelPLang.grid(row=2, column=0)
	entryPName.grid(row=0, column=1)
	entryPDesc.grid(row=1, column=1)
	entryPLang.grid(row=2, column=1)

	buttonClear = Button(gui, text="Clear", fg=color_fg, bg=color_bg, command=clear)
	buttonSubmit = Button(gui, text="Submit", fg=color_fg, bg=color_bg, command=submit)
	buttonExit = Button(gui, text="Exit", fg=color_fg, bg=color_bg, command=exit)
	buttonClear.grid(row=3, column=0)
	buttonSubmit.grid(row=3, column=1)
	buttonExit.grid(row=3, column=2)

	table = Table(gui, 4, projects)

	gui.mainloop()
