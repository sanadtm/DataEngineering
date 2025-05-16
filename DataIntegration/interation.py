
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

cases_df = pd.read_csv("covid_confirmed_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
census_df = pd.read_csv("acs2017_county_data.csv")

abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
    'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}
latest_cases_col = cases_df.columns[-1]
latest_deaths_col = deaths_df.columns[-1]
cases_df = cases_df[['County Name', 'State', latest_cases_col]].copy()
deaths_df = deaths_df[['County Name', 'State', latest_deaths_col]].copy()

# Task 2  Show column headers (before renaming)
print("cases_df :", cases_df.columns.tolist())
print("deaths_df :", deaths_df.columns.tolist())

cases_df.rename(columns={latest_cases_col: 'Cases'}, inplace=True)
deaths_df.rename(columns={latest_deaths_col: 'Deaths'}, inplace=True)
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].copy()
census_df.rename(columns={'County': 'County Name'}, inplace=True)
print("census_df columns:", census_df.columns.tolist())
cases_df['County Name'] = cases_df['County Name'].str.rstrip()
deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()


wash_cases = cases_df[cases_df['County Name'] == 'Washington County']
wash_deaths = deaths_df[deaths_df['County Name'] == 'Washington County']
print("Washington County in cases_df:", len(wash_cases))
print("Washington County in deaths_df:", len(wash_deaths))

# Remove 'Statewide Unallocated' rows from cases_df and deaths_df
cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']


print("cases_df:", len(cases_df))
print("deaths_df:", len(deaths_df))
print("Total 'Washington County' entries across both datasets:", len(pd.concat([wash_cases, wash_deaths]).drop_duplicates()))

combined_df = pd.merge(cases_df, deaths_df, on=['County Name', 'State'])
combined_df['State'] = combined_df['State'].map(abbrev)

# Normalize for merging
combined_df['County Name'] = combined_df['County Name'].str.strip().str.lower()
combined_df['State'] = combined_df['State'].str.strip().str.lower()
census_df['County Name'] = census_df['County Name'].str.strip().str.lower()
census_df['State'] = census_df['State'].str.strip().str.lower()

# Merge all data
merged_df = pd.merge(combined_df, census_df, on=['County Name', 'State'])

# Compute per capita values
merged_df['CasesPerCap'] = merged_df['Cases'] / merged_df['TotalPop']
merged_df['DeathsPerCap'] = merged_df['Deaths'] / merged_df['TotalPop']

# Reorder columns
final_df = merged_df[['County Name', 'State', 'Cases', 'Deaths', 'CasesPerCap', 'DeathsPerCap',
                      'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

final_df.to_csv("combined_output.csv", index=False)
print("combined_output.csv has been created successfully.")

cases_df['key'] = cases_df['County Name'].str.strip().str.lower() + "," + cases_df['State'].str.strip().str.lower()
deaths_df['key'] = deaths_df['County Name'].str.strip().str.lower() + "," + deaths_df['State'].str.strip().str.lower()
census_df['key'] = census_df['County Name'].str.strip().str.lower() + "," + census_df['State'].str.strip().str.lower()

cases_df.set_index('key', inplace=True)
deaths_df.set_index('key', inplace=True)
census_df.set_index('key', inplace=True)

print("\n census_df with key index:")
print(census_df.head())

if '2023-07-23' in cases_df.columns:
    cases_df.rename(columns={'2023-07-23': 'Cases'}, inplace=True)
if '2023-07-23' in deaths_df.columns:
    deaths_df.rename(columns={'2023-07-23': 'Deaths'}, inplace=True)

print("\n Column headers after renaming:")
print("cases_df:", cases_df.columns.values.tolist())
print("deaths_df:", deaths_df.columns.values.tolist())

join_df = cases_df.join(deaths_df, lsuffix='_cases', rsuffix='_deaths')
join_df = join_df.join(census_df)
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']
print("\n Number of rows in join_df:", len(join_df))

correlation_matrix = final_df.corr(numeric_only=True)
print("\n Correlation Matrix:")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig("corrlationHeatmap.png")
