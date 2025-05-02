import pandas as pd

# Load the CSV file
df = pd.read_csv("bc_trip259172515_230215.csv")
# print number of records
print("Number of records:", len(df))                  

# filter the columns
df = df.drop(columns=["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"])
print(df.head())