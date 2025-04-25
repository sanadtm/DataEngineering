import pandas as pd

# Load the dataset
df = pd.read_csv("employees.csv")

#get city counts
city_counts = {}
for i in range(len(df)):
    city = df['city'][i]
    if pd.notna(city):
        if city not in city_counts:
            city_counts[city] = 1
        else:
            city_counts[city] += 1

valid_city_min = True
for city in city_counts:
    if city_counts[city] <= 1:
        valid_city_min = False
        break
print("Assertion 1:Each city has more than one employee.") 
if valid_city_min:
    print('valid') 
else: 
    print ("Invalid")

valid_city_max = True
for city in city_counts:
    if city_counts[city] > 100:
        valid_city_max = False
        break
print("Assertion 2:No city has more than 100 employees.")
if valid_city_max:
    print('valid') 
else: 
    print ("Invalid")
