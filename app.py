from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkCheckBox, CTkTextbox
import pandas as pd
from db import *  # Ensure this module contains `import_from_mysql`, `import_from_csv`, `import_from_mongo`
from tkinter import filedialog, messagebox
import threading

# Initialize the app
app = CTk()
app.title("BI")
app.geometry("800x500")

# Configure the grid layout
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Navigation Frame (Left Panel)
nav_frame = CTkFrame(app, width=200, corner_radius=0)
nav_frame.grid(row=0, column=0, sticky="nswe")
nav_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)  # Add equal spacing
nav_frame.grid_rowconfigure(5, weight=10)  # For extra space at the bottom

# Content Frame (Right Panel)
content_frame = CTkFrame(app, corner_radius=0)
content_frame.grid(row=0, column=1, sticky="nswe")

# Initialize the checkboxes (persistent instances)
checkbox_mysql = CTkCheckBox(content_frame, text="MySQL Data", state="disabled")
checkbox_csv = CTkCheckBox(content_frame, text="CSV Data", state="disabled")
checkbox_mongo = CTkCheckBox(content_frame, text="MongoDB Data", state="disabled")

# Initialize merged data storage and display
merged_data = pd.DataFrame()
merged_data_display = CTkTextbox(content_frame, width=400, height=200, state="disabled")


def show_checkboxes():
    checkbox_mysql.grid(row=0, column=0, pady=10, padx=20, sticky="w")
    checkbox_csv.grid(row=1, column=0, pady=10, padx=20, sticky="w")
    checkbox_mongo.grid(row=2, column=0, pady=10, padx=20, sticky="w")
    merged_data_display.grid(row=6, column=0, pady=10, padx=20, sticky="nsew")


def hide_checkboxes():
    checkbox_mysql.grid_remove()
    checkbox_csv.grid_remove()
    checkbox_mongo.grid_remove()
    merged_data_display.grid_remove()


def update_merged_data_display():
    merged_data_display.configure(state="normal")
    merged_data_display.delete("1.0", "end")
    if not merged_data.empty:
        merged_data_display.insert("1.0", merged_data.head().to_string(index=False))
    else:
        merged_data_display.insert("1.0", "No data loaded yet.")
    merged_data_display.configure(state="disabled")


def print_merged_data():
    print(merged_data)


# Function to update the content based on the button clicked
def show_content(section_name):
    for widget in content_frame.winfo_children():
        if widget not in [checkbox_mysql, checkbox_csv, checkbox_mongo, merged_data_display]:
            widget.destroy()  # Clear previous content except checkboxes and merged data display

    if section_name == "Data Ingestion":
        # Add buttons for data ingestion
        btn_mysql = CTkButton(content_frame, text="Import from MySQL", command=lambda: threading.Thread(target=load_mysql_data).start())
        btn_mysql.grid(row=3, column=0, pady=10, padx=20)

        btn_csv = CTkButton(content_frame, text="Import from CSV", command=lambda: threading.Thread(target=load_csv_data).start())
        btn_csv.grid(row=4, column=0, pady=10, padx=20)

        btn_mongo = CTkButton(content_frame, text="Import from MongoDB", command=lambda: threading.Thread(target=load_mongo_data).start())
        btn_mongo.grid(row=5, column=0, pady=10, padx=20)

        btn_print_data = CTkButton(content_frame, text="Print Merged Data", command=print_merged_data)
        btn_print_data.grid(row=6, column=0, pady=10, padx=20)

        # Show checkboxes and merged data display
        show_checkboxes()
        update_merged_data_display()
    else:
        hide_checkboxes()
        label = CTkLabel(content_frame, text=f"Welcome to {section_name} Section")
        label.grid(row=0, column=0, pady=20, padx=20)


def load_csv_data():
    global merged_data
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            csv_data = import_from_csv(file_path)
            if csv_data is not None:
                checkbox_csv.select()
                merged_data = pd.concat([merged_data, csv_data], ignore_index=True)
                update_merged_data_display()
                messagebox.showinfo("Success", "CSV Data Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading CSV data: {e}")


def load_mysql_data():
    global merged_data
    try:
        mysql_data = import_from_mysql()
        if mysql_data is not None:
            checkbox_mysql.select()
            merged_data = pd.concat([merged_data, mysql_data], ignore_index=True)
            update_merged_data_display()
            messagebox.showinfo("Success", "MySQL Data Loaded Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading MySQL data: {e}")


def load_mongo_data():
    global merged_data
    try:
        mongo_data = import_from_mongo("mydb", "mycollection")  # Replace with your DB/collection
        if mongo_data is not None:
            checkbox_mongo.select()
            merged_data = pd.concat([merged_data, mongo_data], ignore_index=True)
            update_merged_data_display()
            messagebox.showinfo("Success", "MongoDB Data Loaded Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading MongoDB data: {e}")


# Add navigation buttons
btn_home = CTkButton(nav_frame, text="Home", command=lambda: show_content("Home"))
btn_home.grid(row=0, column=0, pady=10, padx=20)

btn_about = CTkButton(nav_frame, text="Data Ingestion", command=lambda: show_content("Data Ingestion"))
btn_about.grid(row=1, column=0, pady=10, padx=20)

btn_settings = CTkButton(nav_frame, text="Settings", command=lambda: show_content("Settings"))
btn_settings.grid(row=2, column=0, pady=10, padx=20)

btn_help = CTkButton(nav_frame, text="Help", command=lambda: show_content("Help"))
btn_help.grid(row=3, column=0, pady=10, padx=20)

btn_exit = CTkButton(nav_frame, text="Exit", fg_color="red", command=app.quit)
btn_exit.grid(row=4, column=0, pady=10, padx=20)

content_frame.grid_rowconfigure(6, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# Initial content
show_content("Home")

# Run the app
app.mainloop()
