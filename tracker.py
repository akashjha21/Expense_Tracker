import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------- DATABASE ----------
def connect_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')
    conn.commit()
    return conn

# ---------- FUNCTIONS ----------
def add_expense():
    try:
        amt = float(amount_var.get())
        cat = category_var.get()
        note = note_var.get()
        date = datetime.now().strftime("%Y-%m-%d")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)", 
                       (amt, cat, date, note))
        conn.commit()
        conn.close()
        amount_var.set("")
        category_var.set("")
        note_var.set("")
        messagebox.showinfo("Success", "Expense added successfully!")
        load_expenses()
        update_total()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def load_expenses():
    for row in expense_table.get_children():
        expense_table.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    for row in cursor.fetchall():
        expense_table.insert("", tk.END, values=row)
    conn.close()

def update_total():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    conn.close()
    total_label.config(text=f"Total Expense: ₹{total:.2f}")

def delete_expense():
    selected = expense_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense to delete.")
        return
    item = expense_table.item(selected[0])
    exp_id = item['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", f"Expense ID {exp_id} deleted.")
    load_expenses()
    update_total()

# ---------- GUI ----------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x500")
root.configure(bg="#f4f4f4")

title = tk.Label(root, text="💸 Expense Tracker", font=("Arial", 18, "bold"), bg="#f4f4f4")
title.pack(pady=10)

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10)

# Entry fields
amount_var = tk.StringVar()
category_var = tk.StringVar()
note_var = tk.StringVar()

tk.Label(frame, text="Amount (₹):", bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame, textvariable=amount_var).grid(row=0, column=1, padx=5)

tk.Label(frame, text="Category:", bg="#f4f4f4").grid(row=0, column=2, padx=5, pady=5, sticky="w")
tk.Entry(frame, textvariable=category_var).grid(row=0, column=3, padx=5)

tk.Label(frame, text="Note:", bg="#f4f4f4").grid(row=0, column=4, padx=5, pady=5, sticky="w")
tk.Entry(frame, textvariable=note_var).grid(row=0, column=5, padx=5)

tk.Button(frame, text="➕ Add Expense", command=add_expense, bg="#4caf50", fg="white").grid(row=0, column=6, padx=10)

# Table
columns = ("ID", "Amount", "Category", "Date", "Note")
expense_table = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    expense_table.heading(col, text=col)
    expense_table.column(col, anchor="center")
expense_table.pack(pady=10)

# Total + Delete
bottom_frame = tk.Frame(root, bg="#f4f4f4")
bottom_frame.pack()

total_label = tk.Label(bottom_frame, text="Total Expense: ₹0.00", font=("Arial", 14), bg="#f4f4f4")
total_label.pack(side="left", padx=20)

tk.Button(bottom_frame, text="🗑️ Delete Selected", command=delete_expense, bg="#e53935", fg="white").pack(side="right", padx=20)

# Initial Load
load_expenses()
update_total()

root.mainloop()
