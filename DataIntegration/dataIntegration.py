import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
cases_df = pd.read_csv("covid_confirmed_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
census_df = pd.read_csv("acs2017_county_data.csv")

# State abbreviation map
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

# Extract latest columns
latest_cases_col = cases_df.columns[-1]
latest_deaths_col = deaths_df.columns[-1]

# Select and rename relevant columns
cases_df = cases_df[['County Name', 'State', latest_cases_col]].rename(columns={latest_cases_col: 'Cases'})
deaths_df = deaths_df[['County Name', 'State', latest_deaths_col]].rename(columns={latest_deaths_col: 'Deaths'})
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].rename(columns={'County': 'County Name'})

# Print initial columns
print("cases_df :", cases_df.columns.tolist())
print("deaths_df :", deaths_df.columns.tolist())
print("census_df columns:", census_df.columns.tolist())

# chean whitespace and lowercase
def clean_names(df):
    df['County Name'] = df['County Name'].str.strip()
    df['State'] = df['State'].str.strip()
    return df

cases_df = clean_names(cases_df)
deaths_df = clean_names(deaths_df)

# Check Washington County
wash_cases = cases_df[cases_df['County Name'] == 'Washington County']
wash_deaths = deaths_df[deaths_df['County Name'] == 'Washington County']
print("Washington County in cases_df:", len(wash_cases))
print("Washington County in deaths_df:", len(wash_deaths))

# Remove unallocated
cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
print("cases_df:", len(cases_df))
print("deaths_df:", len(deaths_df))
print("Total 'Washington County' entries across both datasets:", len(pd.concat([wash_cases, wash_deaths]).drop_duplicates()))

# Merge cases and deaths
combined_df = pd.merge(cases_df, deaths_df, on=['County Name', 'State'])

# Expand state abbreviations
combined_df['State'] = combined_df['State'].map(abbrev).fillna(combined_df['State'])

# Normalize for merging
def normalize(df):
    df['County Name'] = df['County Name'].str.lower()
    df['State'] = df['State'].str.lower()
    return df

combined_df = normalize(combined_df)
census_df = normalize(census_df)

# Merge with census
merged_df = pd.merge(combined_df, census_df, on=['County Name', 'State'])

# Per capita metrics
merged_df['CasesPerCap'] = merged_df['Cases'] / merged_df['TotalPop']
merged_df['DeathsPerCap'] = merged_df['Deaths'] / merged_df['TotalPop']

# Final column arrangement
final_df = merged_df[['County Name', 'State', 'Cases', 'Deaths', 'CasesPerCap', 'DeathsPerCap',
                      'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

final_df.to_csv("combined_output.csv", index=False)
print("combined_output.csv has been created successfully.")

# Set key index for join version
def make_key(df):
    df['key'] = df['County Name'].str.strip().str.lower() + ',' + df['State'].str.strip().str.lower()
    df.set_index('key', inplace=True)
    return df

cases_df = make_key(cases_df)
deaths_df = make_key(deaths_df)
census_df = make_key(census_df)

print("\n census_df with key index:")
print(census_df.head())

# Optional column renaming if column exists
cases_df.rename(columns={'2023-07-23': 'Cases'}, inplace=True, errors='ignore')
deaths_df.rename(columns={'2023-07-23': 'Deaths'}, inplace=True, errors='ignore')

print("\n Column headers after renaming:")
print("cases_df:", cases_df.columns.values.tolist())
print("deaths_df:", deaths_df.columns.values.tolist())

# Join version (just to replicate your original output structure)
join_df = cases_df.join(deaths_df, lsuffix='_cases', rsuffix='_deaths')
join_df = join_df.join(census_df)
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']
print("\n Number of rows in join_df:", len(join_df))

# Correlation matrix and heatmap
correlation_matrix = final_df.corr(numeric_only=True)
print("\n Correlation Matrix:")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig("corrlationHeatmap.png")
print("corrlationHeatmap.png saved.")
