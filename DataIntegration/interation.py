import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
cases_df = pd.read_csv("covid_confirmed_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
census_df = pd.read_csv("acs2017_county_data.csv")

# Define state abbreviations
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

# Extract latest date columns
latest_cases_col = cases_df.columns[-1]
latest_deaths_col = deaths_df.columns[-1]

# Keep relevant columns and rename
cases_df = cases_df[['County Name', 'State', latest_cases_col]].rename(columns={latest_cases_col: 'Cases'})
deaths_df = deaths_df[['County Name', 'State', latest_deaths_col]].rename(columns={latest_deaths_col: 'Deaths'})
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].rename(columns={'County': 'County Name'})

# Strip whitespace
for df in [cases_df, deaths_df, census_df]:
    df['County Name'] = df['County Name'].str.strip().str.lower()
    df['State'] = df['State'].str.strip().str.lower()

# Debug: Count of Washington County
wash_cases = cases_df[cases_df['County Name'] == 'washington county']
wash_deaths = deaths_df[deaths_df['County Name'] == 'washington county']
print("Washington County in cases_df:", len(wash_cases))
print("Washington County in deaths_df:", len(wash_deaths))

# Remove unallocated rows
cases_df = cases_df[cases_df['County Name'] != 'statewide unallocated']
deaths_df = deaths_df[deaths_df['County Name'] != 'statewide unallocated']

# Merge case and death data
combined_df = pd.merge(cases_df, deaths_df, on=['County Name', 'State'])
combined_df['State'] = combined_df['State'].map(lambda x: abbrev.get(x.upper(), x)).str.lower()

# Merge with census
merged_df = pd.merge(combined_df, census_df, on=['County Name', 'State'])

# Per capita metrics
merged_df['CasesPerCap'] = merged_df['Cases'] / merged_df['TotalPop']
merged_df['DeathsPerCap'] = merged_df['Deaths'] / merged_df['TotalPop']

# Reorder columns
final_df = merged_df[['County Name', 'State', 'Cases', 'Deaths', 'CasesPerCap', 'DeathsPerCap',
                      'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

final_df.to_csv("combined_output.csv", index=False)
print("✅ combined_output.csv has been created successfully.")

# Correlation matrix
correlation_matrix = final_df.corr(numeric_only=True)
print("\n📊 Correlation Matrix:")
print(correlation_matrix)

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig("corrlationHeatmap.png")
print("📈 Heatmap saved as corrlationHeatmap.png")
