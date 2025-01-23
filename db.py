import mysql.connector
import pandas as pd
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)

def import_from_mysql():
    try:
        # Replace with your actual database connection details
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pokemongo3!', 
            database='salesdata'
        )
        
        query = "SELECT * FROM sales"  # Replace with your actual SQL query
        df = pd.read_sql(query, connection)
        logging.info("MySQL Data Loaded Successfully!")
        return df
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def import_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info("CSV File Loaded Successfully!")
        return df
    except FileNotFoundError:
        logging.error(f"Error: The file at '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        logging.error("Error: The CSV file is empty.")
        return None
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        return None

def import_from_mongo(db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
    try:
        # Replace with your MongoDB connection URI
        mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
        db_name = "sales"  # Replace with your database name
        collection_name = "orders"  # Replace with your collection name

        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        
        # Fetch all documents and convert to DataFrame
        data = list(collection.find())
        df = pd.DataFrame(data)
        
        # Drop the MongoDB '_id' field if not needed
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        
        logging.info("MongoDB Data Loaded Successfully!")
        return df
    except Exception as e:
        logging.error(f"Error loading data from MongoDB: {e}")
        return None