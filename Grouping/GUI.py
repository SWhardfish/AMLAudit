import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the SQLite database
conn = sqlite3.connect("csv_data.db")
cursor = conn.cursor()

# Create a GUI window
window = tk.Tk()
window.title("CSV Data Viewer")

# Create a treeview widget to display the data
tree = ttk.Treeview(window, columns=("CustomerNo", "Date", "NameAddress", "FFNameAddress", "Similarity", "Status", "Comment"))
tree.heading("#1", text="CustomerNo")
tree.heading("#2", text="Date")
tree.heading("#3", text="NameAddress")
tree.heading("#4", text="FFNameAddress")
tree.heading("#5", text="Similarity")
tree.heading("#6", text="Status")
tree.heading("#7", text="Comment")
tree.pack()

# Function to display data based on 'CustomerNo'
def display_data(customer_no):
    cursor.execute(f"SELECT * FROM csv_data WHERE CustomerNo = {customer_no} ORDER BY CustomerNo")
    data = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert("", "end", values=row)

# Function to save the changes
def save_changes():
    status = "Complete" if reviewed_var.get() == 1 else ""
    comment = comment_entry.get()
    selected_item = tree.selection()
    if selected_item:
        customer_no = tree.item(selected_item[0])["values"][0]
        cursor.execute(f"UPDATE csv_data SET Status = ?, Comment = ? WHERE CustomerNo = ?", (status, comment, customer_no))
        conn.commit()

# Entry widget to input 'CustomerNo'
customer_no_entry = ttk.Entry(window)
customer_no_entry.pack()

# Button to fetch and display data based on 'CustomerNo'
fetch_button = ttk.Button(window, text="Fetch Data", command=lambda: display_data(int(customer_no_entry.get())))
fetch_button.pack()

# Navigation buttons for moving to the next group
next_group_button = ttk.Button(window, text="Next Group")
next_group_button.pack()

# Search box (Only one search box in the UI)
search_box = ttk.Entry(window)
search_box.pack()

# Tick box to confirm group review
reviewed_var = tk.IntVar()
reviewed_checkbox = ttk.Checkbutton(window, text="Group Reviewed", variable=reviewed_var)
reviewed_checkbox.pack()

# Comment box
comment_entry = ttk.Entry(window)
comment_entry.pack()

# Save button to commit changes
save_button = ttk.Button(window, text="Save Changes", command=save_changes)
save_button.pack()

window.mainloop()

# Close the database connection when the GUI is closed
conn.close()
