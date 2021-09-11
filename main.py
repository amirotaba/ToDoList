from tkinter import *
import sqlite3
import tkinter.ttk as ttk


root = Tk()

root.title('To Do List')
root.geometry('320x210')


# functions


# dbconn = sqlite3.connect('task.db')

# curr = dbconn.cursor()
# create table

# c.execute("""CREATE TABLE user_tasks(
#           task text
# )""")

# create done table

# c.execute("""CREATE TABLE done_tasks(
#           task text
# )""")

# dbconn.commit()
# dbconn.close()


def addtask():
    dbconn = sqlite3.connect('task.db')
    curr = dbconn.cursor()
    curr.execute("INSERT INTO user_tasks VALUES(:task_entry)", {'task_entry':task_entry.get()})
    dbconn.commit()
    dbconn.close()

    root.geometry('320x480')
    task_entry.delete(0, END)
    show()
    Error.grid_remove()


def show():
    dbconn = sqlite3.connect('task.db')
    curr = dbconn.cursor()
    curr.execute('SELECT *,oid FROM user_tasks')
    records = curr.fetchall()
    table = ttk.Treeview(root)
    table.grid(row=5, column=0, padx=30, pady=5)
    table['columns'] = ('#1')
    table.column('#0', width=100, minwidth=100)
    table.column('#1', width=150, minwidth=150)

    table.heading('#0', text='ID', anchor=N)
    table.heading('#1', text='Task', anchor=N)

    i = 0
    for record in records:
        row = table.insert('', i, text=record[1], values=(record[0]))
        i = i+1

    dbconn.commit()
    dbconn.close()

    clear_task_button = Button(root, text="Clear all tasks", command=clear_tasks)
    clear_task_button.grid(row=7, column=0, ipadx=10, pady=10)

    check_title.grid(row=0, column=1, pady=10, sticky="W")
    check_label.grid(row=1, column=1, ipadx=10, padx=5, pady=5, sticky="W")
    check_entry.grid(row=1, column=1, pady=10, padx=20)
    check_button.grid(row=2, column=1, ipadx=25)
    check_all.grid(row=3, column=1, ipadx=10)

    root.geometry("630x515")
    task_entry.delete(0, END)


def check():
    dbconn = sqlite3.connect('task.db')
    curr = dbconn.cursor()
    try:
        curr.execute("""INSERT INTO done_tasks 
             SELECT * FROM user_tasks 
             WHERE oid="""+check_entry.get())
        curr.execute("""DELETE FROM user_tasks 
             WHERE oid="""+check_entry.get())
        Error.grid_remove()
    except Exception:
        Error.grid(row=8, column=1, padx=30, pady=0)
    curr.execute('SELECT *,oid FROM done_tasks')
    recordsdone = curr.fetchall()
    table2 = ttk.Treeview(root)
    table2.grid(row=5, column=1, padx=30, pady=5)
    table2['columns'] = ('#1')
    table2.column('#0', width=100, minwidth=100)
    table2.column('#1', width=150, minwidth=150)

    table2.heading('#0', text='ID', anchor=N)
    table2.heading('#1', text='Task', anchor=N)

    i = 0
    for record in recordsdone:
        row2 = table2.insert('', i, text=record[1], values=(record[0]))
        i = i + 1

    dbconn.commit()
    dbconn.close()

    clear_done_button = Button(root, text='Clear done tasks', padx=0, pady=0, command=clear_done)
    clear_done_button.grid(row=7, column=1, ipadx=10, ipady=2, pady=5)

    check_entry.delete(0, END)
    show()


def check_all():
    dbconn = sqlite3.connect('task.db')
    curr = dbconn.cursor()

    curr.execute("""INSERT INTO done_tasks 
                SELECT * FROM user_tasks""")
    curr.execute("DELETE FROM user_tasks")
    Error.grid_remove()
    curr.execute('SELECT *,oid FROM done_tasks')
    recordsdone = curr.fetchall()
    table2 = ttk.Treeview(root)
    table2.grid(row=5, column=1, padx=30, pady=5)
    table2['columns'] = ('#1')
    table2.column('#0', width=100, minwidth=100)
    table2.column('#1', width=150, minwidth=150)

    table2.heading('#0', text='ID', anchor=N)
    table2.heading('#1', text='Task', anchor=N)

    i = 0
    for record in recordsdone:
        row2 = table2.insert('', i, text=record[1], values=(record[0]))
        i = i + 1

    dbconn.commit()
    dbconn.close()

    clear_done_button = Button(root, text='Clear done tasks', padx=0, pady=0, command=clear_done)
    clear_done_button.grid(row=7, column=1, ipadx=10, ipady=2, pady=5)

    check_entry.delete(0, END)
    show()

def clear_tasks():
    dbconn = sqlite3.connect('task.db')

    curr = dbconn.cursor()

    curr.execute("DELETE FROM user_tasks")
    curr.execute("DELETE FROM done_tasks")

    dbconn.commit()
    dbconn.close()

    check()

    Error.grid_remove()


def clear_done():
    dbconn = sqlite3.connect('task.db')

    curr = dbconn.cursor()

    curr.execute("DELETE FROM done_tasks")

    dbconn.commit()
    dbconn.close()

    check()
    Error.grid_remove()


# making labels, buttons and grids
adding_label = Label(root, text='Add new task                                 \n _____________________________')
task_label = Label(root, text='Enter your task: ',)
task_entry = Entry(root,)

task_button = Button(root, text='Add task', padx=30, pady=5, command=addtask)

check_title = Label(root, text='Check done tasks                            \n _____________________________')

show_tasks = Button(root, text='Show all tasks', command=show)

check_label = Label(root, text='Enter ID: ')
check_entry = Entry(root,)
check_button = Button(root, text='Check item', command=check)
check_all = Button(root, text='Check all', command=check_all)

Error = Label(root, text="This id doesn't exist")


adding_label.grid(row=0, column=0, pady=10, sticky="W")
task_label.grid(row=1, column=0, padx=10, pady=0, sticky="W")
task_entry.grid(row=1, column=0, ipadx=20, ipady=5, padx=20, pady=10, sticky="E")
task_button.grid(row=2, column=0, ipadx=70, padx=30, pady=5)

show_tasks.grid(row=3, column=0, ipadx=20, padx=30, pady=5)

check_title.grid(row=5, column=0, pady=10, sticky="W")
check_label.grid(row=7, column=0, ipadx=10, padx=5, pady=5, sticky="W")
check_entry.grid(row=7, column=0, ipady=5, pady=10, padx=20)
check_button.grid(row=8, column=0, ipadx=30, ipady=5)

adding_label.config(font=("Times", 15))

check_title.config(font=("Times", 15))
check_label.config(font=("", 10))
task_label.config(font=("", 10))

root.mainloop()
