import pandas as pd
import psycopg2
import logging
import uuid  # Add import for uuid

logging.basicConfig(level=logging.INFO)

# Function to upload data to PostgreSQL
def upload_to_postgresql(df, host, port, database, user, password):
    try:
        logging.debug(f"DataFrame columns: {df.columns.tolist()}")  # Log the DataFrame columns

        required_columns = {
            'Customer_Dim': ['customer_id', 'customer', 'city', 'state', 'country', 'zip'],
            'Category_Dim': ['category', 'subcategory'],
            'Product_Dim': ['product_name', 'manufactory', 'category', 'subcategory'],
            'Date_Dim': ['order_date', 'ship_date'],
            'Region_Dim': ['region', 'country'],
            'Sales_Fact': ['order_id', 'customer_id', 'product_name', 'manufactory', 'category', 'subcategory', 'order_date', 'ship_date', 'region', 'country', 'sales', 'profit', 'quantity', 'discount']
        }

        for table, columns in required_columns.items():
            missing_columns = set(columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing columns for {table}: {', '.join(missing_columns)}")

        # Establish a connection to the PostgreSQL database
        with psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        ) as conn:
            with conn.cursor() as cursor:
                # Insert data into Customer_Dim table
                customer_data = df[['customer_id', 'customer', 'city', 'state', 'country', 'zip']].drop_duplicates()
                for index, row in customer_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Customer_Dim (customer_id, customer_name, city, state, country, zip)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (customer_id) DO NOTHING
                    """, (row['customer_id'], row['customer'], row['city'], row['state'], row['country'], row['zip']))

                # Insert data into Category_Dim table
                category_data = df[['category', 'subcategory']].drop_duplicates()
                category_data['category_id'] = [str(uuid.uuid4()) for _ in range(len(category_data))]  # Generate category_id
                for index, row in category_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Category_Dim (category_id, category, subcategory)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (category_id) DO NOTHING
                    """, (row['category_id'], row['category'], row['subcategory']))

                # Insert data into Product_Dim table
                product_data = df[['product_name', 'manufactory', 'category', 'subcategory']].drop_duplicates()
                product_data = product_data.merge(category_data, on=['category', 'subcategory'], how='left')
                product_data['product_id'] = [str(uuid.uuid4()) for _ in range(len(product_data))]  # Generate product_id
                
                # Handle unknown product data
                default_category_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO Category_Dim (category_id, category, subcategory)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (category_id) DO NOTHING
                """, (default_category_id, 'Unknown', 'Unknown'))
                
                product_data.loc[product_data['category_id'].isnull(), 'category_id'] = default_category_id
                
                for index, row in product_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Product_Dim (product_id, product_name, manufactory, category_id)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (product_id) DO NOTHING
                    """, (row['product_id'], row['product_name'], row['manufactory'], row['category_id']))

                # Insert data into Date_Dim table
                date_data = df[['order_date', 'ship_date']].drop_duplicates()
                date_data['date_id'] = range(1, len(date_data) + 1)  # Generate date_id
                date_data['year'] = date_data['order_date'].dt.year
                date_data['quarter'] = date_data['order_date'].dt.quarter
                date_data['month'] = date_data['order_date'].dt.month
                date_data['day'] = date_data['order_date'].dt.day
                for index, row in date_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Date_Dim (date_id, order_date, ship_date, year, quarter, month, day)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (date_id) DO NOTHING
                    """, (row['date_id'], row['order_date'], row['ship_date'], row['year'], row['quarter'], row['month'], row['day']))

                # Insert data into Region_Dim table
                region_data = df[['region', 'country']].drop_duplicates()
                region_data['region_id'] = range(1, len(region_data) + 1)  # Generate region_id
                for index, row in region_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Region_Dim (region_id, region, country)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (region_id) DO NOTHING
                    """, (row['region_id'], row['region'], row['country']))

                # Insert data into Sales_Fact table
                sales_data = df.merge(product_data, on=['product_name', 'manufactory', 'category', 'subcategory'], how='left')
                sales_data = sales_data.merge(date_data, on=['order_date', 'ship_date'], how='left')
                sales_data = sales_data.merge(region_data, on=['region', 'country'], how='left')
                for index, row in sales_data.iterrows():
                    cursor.execute("""
                        INSERT INTO Sales_Fact (order_id, customer_id, product_id, date_id, region_id, sales, profit, quantity, discount)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (order_id) DO NOTHING
                    """, (row['order_id'], row['customer_id'], row['product_id'], row['date_id'], row['region_id'], row['sales'], row['profit'], row['quantity'], row['discount']))

                # Commit the transaction
                conn.commit()
                logging.info("Data inserted successfully into the PostgreSQL database.")

    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")

# Example usage
if __name__ == "__main__":
    # Load your cleaned dataset (replace 'cleaned_data.csv' with your file path)
    cleaned_data = pd.read_csv('cleaned_data.csv')

    # PostgreSQL database details
    pg_host = "localhost"
    pg_port = "5432"
    pg_database = "Sales"
    pg_user = "postgres"
    pg_password = "pokemongo"

    # Upload data to PostgreSQL
    upload_to_postgresql(cleaned_data, pg_host, pg_port, pg_database, pg_user, pg_password)
