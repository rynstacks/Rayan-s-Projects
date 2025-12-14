import tkinter as tk
from tkinter import messagebox
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="task_manager"
)
cur = conn.cursor()

#.strip to remove space
#adding tasks here
def add_task():
    date = entry_date.get().strip()
    time = entry_time.get().strip()
    name = entry_name.get().strip()
    desc = text_desc.get("1.0", tk.END).strip()
    important = important_var.get()

    if name.lower() == "rayan aslam": #small easter egg
        messagebox.showinfo("Welcome, creator")

    if not date or not time or not name:
        messagebox.showerror("Error", "Date, Time and Task Name are required")
        return

    cur.execute(
        "INSERT INTO tasks (task_date, task_time, task_name, task_description, important) "
        "VALUES (%s, %s, %s, %s, %s)",
        (date, time, name, desc, important)
    )
    conn.commit()#perm save

    messagebox.showinfo("Task added to Database")#mssg after for gui
    view_tasks()

#show tasks w/ button
def view_tasks():
    task_list.delete(0, tk.END)
    selected_date = filter_date.get().strip()

    if not selected_date:
        messagebox.showerror("Error", "Please enter a date(correct format)")
        return
    cur.execute(
        "SELECT id, task_time, task_name, status "
        "FROM tasks WHERE task_date = %s ORDER BY task_time",#order by time 
        (selected_date,)
    )
    rows = cur.fetchall()

    if not rows:
        task_list.insert(tk.END, "No tasks found")
        return

    for row in rows:
        task_list.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

#remove takss
def delete_task():
    selected = task_list.curselection()
    if not selected:
        return

    task_id = task_list.get(selected).split(" | ")[0]

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    view_tasks()

#finished tasks w/ button
def mark_done():
    selected = task_list.curselection()
    if not selected:
        return

    task_id = task_list.get(selected).split(" | ")[0]

    cur.execute("UPDATE tasks SET status = 'done' WHERE id = %s", (task_id,))
    conn.commit()
    view_tasks()

#SHOW ALL TASKSS

def show_all_tasks():
    task_list.delete(0, tk.END)

    #ascending
    cur.execute(
        "SELECT id, task_date, task_time, task_name, status "
        "FROM tasks ORDER BY id ASC"
    )

    rows = cur.fetchall()

    if not rows:
        task_list.insert(tk.END, "No tasks found")
        return

    for row in rows:
        task_list.insert(
            tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}"
        )




#gui interface with tkinter
    
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x670")#670
root.configure(bg="#2B2B2B")

tk.Label(root, text="Date (YYYY-MM-DD)", bg="#2B2B2B", fg="white").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Label(root, text="Time (HH:MM)", bg="#2B2B2B", fg="white").pack()
entry_time = tk.Entry(root)
entry_time.pack()

tk.Label(root, text="Task Name", bg="#2B2B2B", fg="white").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Task Description", bg="#2B2B2B", fg="white").pack()
text_desc = tk.Text(root, height=4)
text_desc.pack()



important_var = tk.IntVar()
tk.Checkbutton(
    root, text="Important",
    variable=important_var,
    bg="#2B2B2B", fg="white"
).pack()

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)

tk.Label(root, text="View Tasks for Date", bg="#2B2B2B", fg="white").pack()
filter_date = tk.Entry(root)
filter_date.pack()

tk.Button(root, text="View Tasks", command=view_tasks).pack(pady=5)

tk.Button(root, text="Show All Tasks", command=show_all_tasks).pack(pady=5)

task_list = tk.Listbox(root, width=70)
task_list.pack(pady=10)

tk.Button(root, text="Mark as Done ✔", command=mark_done).pack(pady=2)
tk.Button(root, text="Delete Task ❌", command=delete_task).pack(pady=2)

tk.Label(
    root,
    text="Task Manager by Rayan Aslam",
    bg="#2B2B2B",      # same dark grey background
    fg="white"          # white text
).pack(side=tk.BOTTOM, pady=10)

root.mainloop()

#ty for using my program!
#Rayan Aslam
#XII B
