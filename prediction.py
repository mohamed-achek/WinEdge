import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Function to fetch data from CSV
def fetch_data():
    df = pd.read_csv('superstore_dataset.csv', usecols=['order_date', 'sales'])
    return df

# Function to preprocess data
def preprocess_data(df):
    # Convert order_date to datetime and extract year and month
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month

    # Handle missing values
    df.fillna(0, inplace=True)

    return df

# Function to train the model on year 2022 data
def train_model(df):
    # Filter data for the year 2022
    df_2022 = df[df['year'] == 2022]
    X = df_2022[['year', 'month']]
    y = df_2022['sales']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2}")

    return model

# Function to predict total sales for 2023
def predict_total_sales_2023(model, df):
    # Generate features for 2023
    next_year = 2023
    months = np.arange(1, 13)
    features = pd.DataFrame({'year': next_year, 'month': months})

    # Predict sales
    predictions = model.predict(features)
    total_sales_2023 = predictions.sum()

    return round(total_sales_2023, 2)

# Main function
def main():
    # Fetch data
    df = fetch_data()

    # Preprocess data
    df = preprocess_data(df)

    # Train model
    model = train_model(df)

    # Predict total sales for 2023
    total_sales_2023 = predict_total_sales_2023(model, df)

    # Display the total sales for 2023
    print(f"Total Sales for 2023: {total_sales_2023}")

if __name__ == "__main__":
    main()
