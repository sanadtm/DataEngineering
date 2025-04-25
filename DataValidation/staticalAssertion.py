import pandas as pd
import matplotlib.pyplot as plt

# Load employee data
df = pd.read_csv("employees.csv")

df['salary_millions'] = df['salary'] / 1_000_000


plt.figure(figsize=(10, 6))
plt.hist(df['salary_millions'], bins=50, color='orange', edgecolor='black')
plt.title("Histogram of Salaries (in Millions)")
plt.xlabel("Salary (Millions USD)")
plt.ylabel("Employees")
plt.grid(True)
plt.tight_layout()
plt.savefig("salary_histogram.png")


total = len(df)
under_200k = (df['salary'] < 200000).sum()
percent = (under_200k / total) * 100
print(f"{percent:.2f}%")
if percent >= 90:
    print("The dataset is Valid.")
else:
    print("The dataset is Invalid.")
