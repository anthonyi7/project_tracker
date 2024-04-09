import tkinter as tk
from tkinter import ttk
import json

class SupportCaseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Support Case Tracker")
        self.create_widgets()
        self.root.bind('<Double-1>', self.toggle_state)  # Bind double-click event to toggle state
        self.tree.bind('<Button-1>', self.check_blank_area)  # Bind single-click event to check for blank area
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Ensure data is saved when the window is closed

    def create_widgets(self):
        # Input fields for Case # and Description
        tk.Label(self.root, text="Case #").grid(row=0, column=0)
        self.case_number_entry = tk.Entry(self.root)
        self.case_number_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Description").grid(row=0, column=2)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=0, column=3)

        # Button to add a new case
        self.add_button = tk.Button(self.root, text="Add Case", command=self.add_case)
        self.add_button.grid(row=0, column=4)

        # Button to delete a selected case
        self.delete_button = tk.Button(self.root, text="Delete Case", command=self.delete_case)
        self.delete_button.grid(row=0, column=5)

        # Treeview setup
        self.columns = ("Case #", "Description", "Response Inbound", "Needs Research", "Needs Response Today", "Response Sent", "Close EOD")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.grid(row=1, column=0, columnspan=6, sticky='nsew')

        # Define tags for coloring rows
        self.tree.tag_configure('green', background='lightgreen')
        self.tree.tag_configure('yellow', background='yellow')
        self.tree.tag_configure('lightpink', background='lightpink1')
        self.load_data()  # Load data from JSON file

    def add_case(self):
        case_number = self.case_number_entry.get()
        description = self.description_entry.get()
        if case_number and description:  # Ensure fields are not empty
            row_data = (case_number, description, "❌❌", "❌❌", "❌❌", "❌❌", "❌❌")  # Initial state
            iid = self.tree.insert("", tk.END, values=row_data)
            self.update_row_color(iid)  # Update row color based on the initial state
            self.case_number_entry.delete(0, tk.END)  # Clear input fields
            self.description_entry.delete(0, tk.END)

    def toggle_state(self, event):
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify_column(event.x)
        if item and column in ['#3', '#4', '#5', '#6', '#7']:  # Only toggle state for certain columns
            cur_value = self.tree.item(item, 'values')[int(column[1:]) - 1]
            new_value = "✅" if cur_value == "❌❌" else "❌❌"
            values = list(self.tree.item(item, 'values'))
            values[int(column[1:]) - 1] = new_value
            self.tree.item(item, values=values)
            self.update_row_color(item)  # Update row color based on new state

    def update_row_color(self, item):
        values = self.tree.item(item, 'values')
        # Reset to default first to avoid color conflict
        self.tree.item(item, tags=())
        # Check and apply color based on the specific conditions
        if values[6] == "✅":  # If "Close EOD" is checked
            self.tree.item(item, tags=('green',))
        elif values[2] == "✅":  # If "Response Inbound" is checked
            self.tree.item(item, tags=('lightpink',))  # Assuming 'orange' meant to be lightpink1 for "Response Inbound"
        elif values[3] == "✅" or values[4] == "✅":  # If "Needs Research" or "Needs Response Today" is checked
            self.tree.item(item, tags=('yellow',))    
        else:
            self.tree.item(item, tags=())  # Reset to default if none of the conditions are met

    def check_blank_area(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            self.tree.selection_remove(self.tree.selection())

    def delete_case(self):
        selected_items = self.tree.selection()  # Get the selected items
        for item in selected_items:
            self.tree.delete(item)  # Delete each selected item

    def save_data(self):
        items = self.tree.get_children()
        data = []
        for item in items:
            row = self.tree.item(item, 'values')
            data.append(row)
        with open('case_data.json', 'w') as outfile:
            json.dump(data, outfile)

    def load_data(self):
        try:
            with open('case_data.json', 'r') as infile:
                data = json.load(infile)
                for row in data:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            pass  # File not found, skip loading data

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SupportCaseTracker(root)
    root.mainloop()