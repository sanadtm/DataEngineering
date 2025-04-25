import pandas as pd

# Read the employee data
df = pd.read_csv("employees.csv")

missing_name_count = 0
for name in df['name']:
    if pd.isnull(name):
        missing_name_count += 1
print("Records with missing names:", missing_name_count)

phone_count = 0
for phone in df['phone']:
    phone_str = str(phone)
    digits_only = ''.join(c for c in phone_str if c.isdigit())
    if len(digits_only) < 10:
        phone_count += 1

print("Phone numbers with less than 10 digits:", phone_count)
