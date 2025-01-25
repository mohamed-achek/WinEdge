from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkTextbox
import psycopg2
from tkinter import messagebox

# Function to query data from PostgreSQL
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
        conn.close()
        return data
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while querying data: {e}")
        return []

# Function to display data in a popup
def display_data(data, title):
    popup = CTk()
    popup.title(title)
    popup.geometry("600x400")
    textbox = CTkTextbox(popup, width=580, height=380)
    textbox.pack(pady=10, padx=10)
    for row in data:
        textbox.insert("end", f"{row}\n")
    textbox.configure(state="disabled")
    popup.mainloop()

# Query functions
def query_sales():
    query = "SELECT * FROM Sales_Fact ORDER BY sales DESC LIMIT 10"
    data = query_data(query)
    display_data(data, "Top 10 Sales")

def query_profit():
    query = "SELECT * FROM Sales_Fact ORDER BY profit DESC LIMIT 10"
    data = query_data(query)
    display_data(data, "Top 10 Profit")

def query_quantity():
    query = "SELECT * FROM Sales_Fact ORDER BY quantity DESC LIMIT 10"
    data = query_data(query)
    display_data(data, "Top 10 Quantity")

# Initialize the app
app = CTk()
app.title("ROLAP Queries")
app.geometry("300x200")

# Create buttons for each query
btn_sales = CTkButton(app, text="Query Sales", command=query_sales)
btn_sales.pack(pady=10, padx=20)

btn_profit = CTkButton(app, text="Query Profit", command=query_profit)
btn_profit.pack(pady=10, padx=20)

btn_quantity = CTkButton(app, text="Query Quantity", command=query_quantity)
btn_quantity.pack(pady=10, padx=20)

# Run the app
app.mainloop()
