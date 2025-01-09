import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()
TOKEN_DB=os.getenv('ASTRA_DB_TOKEN')
CLIENT_ID=os.getenv('ASTRA_DB_CLIENT_ID')
def plot_graph(x_axis,y_axis,start_date="2024-08-30",end_date="2024-07-01"):

  # Initialize the client
  client = DataAPIClient(TOKEN_DB)
  db = client.get_database_by_api_endpoint(
    CLIENT_ID
  )

  print(f"Connected to Astra DB: {db.list_collection_names()}")

  collection = db.get_collection("cwc_vectordb")
  dict_data={}
  try:
      query_results = collection.find({})  # Empty filter to retrieve all documents (limit as needed)
      dict_data = list(query_results)
  except Exception as e:
      print(f"An error occurred while querying the database: {e}")
  df = pd.DataFrame(dict_data)

  # Display the columns of the DataFrame
  print(df.columns)




  # Load the data from the CSV file
  # df = pd.read_csv('./cwc_vectordb.csv')

  # Convert the 'timestamp' column to datetime
  df['timestamp'] = pd.to_datetime(df['timestamp'])

  # Create a new 'Date' column in the format 'dd-mm-yyyy'
  df["Date"] = df["timestamp"].apply(lambda x: x.strftime('%Y-%m-%d'))

#   # Get start and end dates from the user (Example input)
#   start_date = "2024-07-01"  # Input from user
#   end_date = "2024-08-30"    # Input from user

  # Convert user-provided dates to datetime
  start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
  end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
  df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

  # Filter rows based on the date range (inclusive)
  df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

  # Sort the data with respect to the date
  df = df.sort_values(by='Date')

  # Ensure required columns exist
  required_columns = ['Date', 'likesCount', 'commentsCount']
  missing_columns = [col for col in required_columns if col not in df.columns]

  if missing_columns:
      st.error(f"The following required columns are missing in the DataFrame: {', '.join(missing_columns)}")
  else:
      # Set up the plot
      plt.figure(figsize=(12, 6))
      
      # Plot each metric with different colors
      plt.plot(df['Date'], df['likesCount']/100, label='Likes', color='blue')
      plt.plot(df['Date'], df['commentsCount'], label='Comments', color='red')
      
      # Add labels and legend
      plt.title("Metrics Over Time", fontsize=16)
      plt.xlabel("Date", fontsize=12)
      plt.ylabel("Values", fontsize=12)
      plt.legend()
      plt.grid(True)

      # Display the plot in Streamlit
      st.pyplot(plt)