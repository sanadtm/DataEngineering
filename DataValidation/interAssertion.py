import pandas as pd

# Load employee data
df = pd.read_csv("employees.csv")

known_ids = list(df['eid'])

missing_manager_count = 0
for i in range(len(df)):
    manager_id = df['reports_to'][i]
    if pd.notna(manager_id):
        if manager_id not in known_ids:
            missing_manager_count += 1
print("Employees with unknown managers:", missing_manager_count)

missing_reports_to = 0
for i in range(len(df)):
    if pd.isna(df['reports_to'][i]):
        missing_reports_to += 1
print("Employees with no manager assigned:", missing_reports_to)
