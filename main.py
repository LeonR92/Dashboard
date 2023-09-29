import streamlit as st
import pandas as pd
import mysql.connector
import os
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="geoapiExercises")

st.title("E-commerce Data Uploader")

df = None  # Initialize df
uploaded_files = st.file_uploader(
    "Choose a CSV file", type="csv", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.write(f"Displaying first few rows of {uploaded_file.name}:")
        st.write(df.head())

        unique_key = f"save_to_mysql_{uploaded_file.name}"

        if st.button("Save to MySQL", key=unique_key):
            try:
                connection = mysql.connector.connect(
                    host=os.environ.get('MYSQL_HOST', 'db'),
                    user=os.environ.get('MYSQL_USER', 'root'),
                    password=os.environ.get('MYSQL_PASSWORD', 'password'),
                    database=os.environ.get('MYSQL_DATABASE', 'ecommerce_db')
                )
                cursor = connection.cursor()
                for _, row in df.iterrows():
                    # Check if product_name already exists
                    cursor.execute(
                        "SELECT * FROM sales WHERE product_name = %s", (row['product_name'],))

                    result = cursor.fetchone()

                    if result:
                        st.warning(
                            f"Product {row['product_name']} already exists in the database!")
                    else:
                        sql = "INSERT INTO sales (`product_name`, `Category`, `Price`, `customer_name`, `City`, `purchase_date`) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, tuple(row))
                        connection.commit()

                st.success("Data saved successfully!")

            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                connection.close()


if df is not None:

    # Bar chart showing total sales by category
    df['Year'] = pd.to_datetime(df['purchase_date']).dt.year

    # Group by year and sum the sales
    yearly_sales = df.groupby('Year')['Price'].sum().reset_index()

    # Bar chart showing total sales per year
    fig6 = px.bar(yearly_sales, x='Year', y='Price',
                  title="Total Sales per Year")
    st.plotly_chart(fig6)

    # Box plot of product prices by category
    fig4 = px.box(df, x='Category', y='Price',
                  title="Product Prices by Category")
    st.plotly_chart(fig4)

    # Group by "Purchase Date" and sum the sales
    agg_sales = df.groupby('purchase_date')['Price'].sum().reset_index()

    # Plotting using plotly
    fig = px.line(agg_sales, x='purchase_date',
                  y='Price', title="Sales Over Time")
    st.plotly_chart(fig)
