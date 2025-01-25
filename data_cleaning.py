from db import *
import pandas as pd
import uuid

def clean_data(extracted_data, update_display_callback):
    if not extracted_data.empty:
        # Remove duplicates
        extracted_data.drop_duplicates(inplace=True)

        # Handle missing values
        extracted_data.fillna(0, inplace=True)  

        # Standardize date formats
        extracted_data['order_date'] = pd.to_datetime(extracted_data['order_date'])
        extracted_data['ship_date'] = pd.to_datetime(extracted_data['ship_date'])

        # Correct data types
        extracted_data['quantity'] = extracted_data['quantity'].astype(int)
        extracted_data['sales'] = extracted_data['sales'].astype(float)
        extracted_data['profit'] = extracted_data['profit'].astype(float)

        # Standardize categorical data (e.g., country names)
        extracted_data['country'] = extracted_data['country'].replace({'US': 'United States', 'USA': 'United States'})

        # Validate data integrity (ensure ship_date is not earlier than order_date)
        extracted_data = extracted_data[extracted_data['ship_date'] >= extracted_data['order_date']]

        # Create a unique customer_id for each customer using UUIDs
        customer_id_map = {}
        for customer in extracted_data['customer'].unique():
            customer_id_map[customer] = str(uuid.uuid4())

        extracted_data['customer_id'] = extracted_data['customer'].map(customer_id_map)

        # Create a unique category_id for each category using UUIDs
        category_id_map = {}
        for category in extracted_data['category'].unique():
            category_id_map[category] = str(uuid.uuid4())

        extracted_data['category_id'] = extracted_data['category'].map(category_id_map)


        # Call the update_display_callback function to refresh the display
        update_display_callback()

        # Print the cleaned data
        print("Cleaned Data:")
        print(extracted_data)

        print("Data cleaned successfully!")
    else:
        print("No data loaded yet.")
