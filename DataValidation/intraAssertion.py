import pandas as pd

# Load employee data
df = pd.read_csv("employees.csv")

# Convert dates
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')

count_wrong_order = 0
for i in range(len(df)):
    birth = df['birth_date'][i]
    hire = df['hire_date'][i]
    if pd.notna(birth) and pd.notna(hire):
        if hire < birth:
            count_wrong_order += 1
print("People hired before they were born:", count_wrong_order)

count_violations = 0
for i in range(len(df)):
    birth = df['birth_date'][i]
    hire = df['hire_date'][i]
    salary = df['salary'][i]

    if pd.notna(birth) and pd.notna(hire):
        age = (hire - birth).days // 365
        if age < 16 or salary > 200000:
            count_violations += 1
print("People under 16 at hire or earning over $200,000:", count_violations)
