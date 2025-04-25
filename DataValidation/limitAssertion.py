import pandas as pd

# Load employee data
df = pd.read_csv("employees.csv")

hired_before_2015 = 0
for date in df['hire_date']:
    if pd.notna(date):
        year = pd.to_datetime(date).year
        if year < 2015:
            hired_before_2015 += 1
print("Employees hired before 2015:", hired_before_2015)

under_150k = 0
for salary in df['salary']:
    if salary < 150000:
        under_150k += 1
print("Employees earning less than $150,000:", under_150k)

outside_range = 0
for salary in df['salary']:
    if not (140000 <= salary <= 149999):
        outside_range += 1
print("Employees NOT earning between $140,000 and $149,999:", outside_range)
