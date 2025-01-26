from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkCheckBox, CTkTextbox, CTkImage
import pandas as pd
from db import *  # Ensure this module contains `import_from_mysql`, `import_from_csv`, `import_from_mongo`
from tkinter import filedialog, messagebox
import threading
from data_cleaning import clean_data
from loading import upload_to_postgresql  # Import the function to upload data to PostgreSQL
import uuid  # Add import for uuid
import psycopg2  # Add import for psycopg2
from tkinter import ttk  # Add import for ttk
from prediction import predict_total_sales_2023  # Import the specific prediction function
from PIL import Image  # Import PIL for image handling

# Initialize the app
app = CTk()
app.title("WinEdge")
app.geometry("800x500")

# Configure the grid layout
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Navigation Frame (Left Panel)
nav_frame = CTkFrame(app, width=200, corner_radius=0)
nav_frame.grid(row=0, column=0, sticky="nswe")
nav_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Add equal spacing
nav_frame.grid_rowconfigure(6, weight=10)  # For extra space at the bottom

# Content Frame (Right Panel)
content_frame = CTkFrame(app, corner_radius=0)
content_frame.grid(row=0, column=1, sticky="nswe")

# Initialize the checkboxes (persistent instances)
checkbox_mysql = CTkCheckBox(content_frame, text="MySQL Data", state="disabled")
checkbox_csv = CTkCheckBox(content_frame, text="CSV Data", state="disabled")
checkbox_mongo = CTkCheckBox(content_frame, text="MongoDB Data", state="disabled")

# Initialize merged data storage and display
merged_data = pd.DataFrame()
extracted_data = pd.DataFrame()
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

    if section_name == "Extraction":
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
    elif section_name == "Transform & Load":
        btn_clean_data = CTkButton(content_frame, text="Clean Data", command=lambda: clean_data(extracted_data, update_merged_data_display))
        btn_clean_data.grid(row=3, column=0, pady=10, padx=20)
        
        btn_load_data = CTkButton(content_frame, text="Load Data to DWH", command=lambda: threading.Thread(target=load_data_to_dwh).start())
        btn_load_data.grid(row=4, column=0, pady=10, padx=20)
        
        # Show checkboxes and merged data display
        show_checkboxes()
        update_merged_data_display()
    elif section_name == "Data Analysis":
        btn_query_sales = CTkButton(content_frame, text="Query Sales", command=query_sales)
        btn_query_sales.grid(row=3, column=0, pady=10, padx=20)

        btn_query_profit = CTkButton(content_frame, text="Query Profit", command=query_profit)
        btn_query_profit.grid(row=4, column=0, pady=10, padx=20)

        btn_query_quantity = CTkButton(content_frame, text="Query Quantity", command=query_quantity)
        btn_query_quantity.grid(row=5, column=0, pady=10, padx=20)
    elif section_name == "Machine Learning":
        btn_predict_sales = CTkButton(content_frame, text="Predict Sales for next year", command=lambda: threading.Thread(target=predict_sales_and_display).start())
        btn_predict_sales.grid(row=3, column=0, pady=10, padx=20)
        
        global sales_label
        sales_label = CTkLabel(content_frame, text="", font=("Arial", 16))
        sales_label.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")
    else:
        hide_checkboxes()
        label = CTkLabel(content_frame, text="Welcome to WinEdge", font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, pady=20, padx=20)

    if section_name == "Home":
        # Load and display the logo
        logo_image = Image.open("Winedge.png")
        logo_image = CTkImage(logo_image, size=(400, 400))
        logo_label = CTkLabel(content_frame, image=logo_image, text="")
        logo_label.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")


def load_csv_data():
    global merged_data, extracted_data
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            csv_data = import_from_csv(file_path)
            if csv_data is not None:
                checkbox_csv.select()
                merged_data = pd.concat([merged_data, csv_data], ignore_index=True)
                extracted_data = merged_data.copy()
                update_merged_data_display()
                messagebox.showinfo("Success", "CSV Data Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading CSV data: {e}")


def load_mysql_data():
    global merged_data, extracted_data
    try:
        mysql_data = import_from_mysql()
        if mysql_data is not None:
            checkbox_mysql.select()
            merged_data = pd.concat([merged_data, mysql_data], ignore_index=True)
            extracted_data = merged_data.copy()
            update_merged_data_display()
            messagebox.showinfo("Success", "MySQL Data Loaded Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading MySQL data: {e}")


def load_mongo_data():
    global merged_data, extracted_data
    try:
        mongo_data = import_from_mongo("mydb", "mycollection")  # Replace with your DB/collection
        if mongo_data is not None:
            checkbox_mongo.select()
            merged_data = pd.concat([merged_data, mongo_data], ignore_index=True)
            extracted_data = merged_data.copy()
            update_merged_data_display()
            messagebox.showinfo("Success", "MongoDB Data Loaded Successfully!")
            # Print the extracted data
            print("Extracted Data:")
            print(extracted_data)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading MongoDB data: {e}")


def load_data_to_dwh():
    global extracted_data  # Ensure we use the global extracted_data
    if extracted_data.empty:
        messagebox.showerror("Error", "No data to load into the data warehouse.")
        return

    # Ensure the customer_id column exists and is of type uuid
    if 'customer_id' not in extracted_data.columns:
        extracted_data['customer_id'] = [str(uuid.uuid4()) for _ in range(len(extracted_data))]

    # DWH server details from loading.py
    server = "localhost"
    database = "Sales"
    username = "postgres"
    password = "pokemongo"
    
    # Upload data to DWH
    try:
        upload_to_dwh(extracted_data, server, database, username, password)
        messagebox.showinfo("Success", "Data loaded to the data warehouse successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data to PostgreSQL: {e}")


def upload_to_dwh(data, server, database, username, password):
    try:
        upload_to_postgresql(data, server, "5432", database, username, password)
        messagebox.showinfo("Success", "Data loaded to DWH successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading data to DWH: {e}")


def query_data(query):
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="Sales",
            user="postgres",
            password="pokemongo"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return data, columns
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while querying data: {e}")
        return [], []


def display_data(data, columns, title):
    if data and columns:
        popup = CTk()
        popup.title(title)
        popup.geometry("800x400")
        
        frame = CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        
        for row in data:
            tree.insert("", "end", values=row)
        
        popup.mainloop()


def query_sales():
    query = "SELECT * FROM Sales_Fact ORDER BY sales DESC LIMIT 10"
    data, columns = query_data(query)
    display_data(data, columns, "Top 10 Sales")


def query_profit():
    query = "SELECT * FROM Sales_Fact ORDER BY profit DESC LIMIT 10"
    data, columns = query_data(query)
    display_data(data, columns, "Top 10 Profit")


def query_quantity():
    query = "SELECT * FROM Sales_Fact ORDER BY quantity DESC LIMIT 10"
    data, columns = query_data(query)
    display_data(data, columns, "Top 10 Quantity")


def predict_sales_and_display():
    import prediction
    df = prediction.fetch_data()
    df = prediction.preprocess_data(df)
    model = prediction.train_model(df)
    total_sales_2023 = prediction.predict_total_sales_2023(model, df)
    sales_label.configure(text=f"Total Sales for 2023: {total_sales_2023:.2f}")


# Add navigation buttons
btn_home = CTkButton(nav_frame, text="Home", command=lambda: show_content("Home"))
btn_home.grid(row=0, column=0, pady=10, padx=20)

btn_about = CTkButton(nav_frame, text="Extraction", command=lambda: show_content("Extraction"))
btn_about.grid(row=1, column=0, pady=10, padx=20)

btn_TL = CTkButton(nav_frame, text="Transform & Load", command=lambda: show_content("Transform & Load"))
btn_TL.grid(row=2, column=0, pady=10, padx=20)

btn_DA = CTkButton(nav_frame, text="Data Analysis", command=lambda: show_content("Data Analysis"))
btn_DA.grid(row=3, column=0, pady=10, padx=20)

btn_ML = CTkButton(nav_frame, text="Machine Learning", command=lambda: show_content("Machine Learning"))
btn_ML.grid(row=4, column=0, pady=10, padx=20)

btn_exit = CTkButton(nav_frame, text="Exit", fg_color="red", command=app.quit)
btn_exit.grid(row=5, column=0, pady=10, padx=20)

content_frame.grid_rowconfigure(6, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# Initial content
show_content("Home")

# Run the app
app.mainloop()
