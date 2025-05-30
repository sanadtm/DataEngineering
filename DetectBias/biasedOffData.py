import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import StringIO
from scipy.stats import binomtest, ttest_1samp, chi2_contingency

# --- Load Data ---
with open("trimet_stopevents_2022-12-07.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

tables = soup.find_all("table")
df_list = [pd.read_html(StringIO(str(table)))[0] for table in tables]
df = pd.concat(df_list, ignore_index=True)

# Clean column names
df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
stops_df = df[["trip_number", "vehicle_number", "arrive_time", "location_id", "ons", "offs"]].copy()
stops_df.rename(columns={"trip_number": "trip_id", "arrive_time": "tstamp"}, inplace=True)

# Convert data types
stops_df = stops_df.astype({
    "trip_id": int, "vehicle_number": int, "tstamp": int,
    "location_id": int, "ons": int, "offs": int
})

# Convert timestamp
base = datetime(2022, 12, 7)
stops_df["tstamp"] = stops_df["tstamp"].apply(lambda x: base + timedelta(seconds=x))


print("\n--- Output ---")
print("Unique Vehicles:", stops_df["vehicle_number"].nunique())
print("Unique Locations:", stops_df["location_id"].nunique())
print("Timestamps:", stops_df["tstamp"].min(), "→", stops_df["tstamp"].max())
boarded = (stops_df["ons"] >= 1).sum()
boarding_percent = boarded / len(stops_df) * 100
print("Total with boarding:", boarded)
print("Percent with boarding: {:.2f}%".format(boarding_percent))


loc_df = stops_df[stops_df["location_id"] == 6913]
print("Location 6913 - Stops:", len(loc_df), "Unique Buses:", loc_df["vehicle_number"].nunique(),
      "Boarding %: {:.2f}%".format((loc_df["ons"] >= 1).mean() * 100))

veh_df = stops_df[stops_df["vehicle_number"] == 4062]
print("Vehicle 4062 - Stops:", len(veh_df), "Boarded:", veh_df["ons"].sum(), "Offs:", veh_df["offs"].sum(),
      "Boarding %: {:.2f}%".format((veh_df["ons"] >= 1).mean() * 100))

overall_p = boarding_percent / 100
biased = []

for vid, group in stops_df.groupby("vehicle_number"):
    total = len(group)
    boarded = (group["ons"] >= 1).sum()
    if total == 0:
        continue
    p_val = binomtest(boarded, total, overall_p).pvalue
    if p_val < 0.05:
        biased.append((vid, p_val))

for vid, p in sorted(biased, key=lambda x: x[1]):
    print(f"Vehicle {vid} → p = {p:.6f}")


rel_df = pd.read_csv("trimet_relpos_2022-12-07.csv")
rel_df.columns = [col.lower().strip() for col in rel_df.columns]

relpos_values = rel_df["relpos"].dropna()
mean_relpos = relpos_values.mean()

gps_biased = []

for vid, group in rel_df.groupby("vehicle_number"):
    vals = group["relpos"].dropna()
    if len(vals) > 1:
        p = ttest_1samp(vals, popmean=mean_relpos).pvalue
        if p < 0.005:
            gps_biased.append((vid, p))

for vid, p in sorted(gps_biased, key=lambda x: x[1]):
    print(f"Vehicle {vid} → p = {p:.6f}")

total_ons = stops_df["ons"].sum()
total_offs = stops_df["offs"].sum()
chi_biased = []

for vid, group in stops_df.groupby("vehicle_number"):
    ons = group["ons"].sum()
    offs = group["offs"].sum()
    observed = [[offs, ons], [total_offs - offs, total_ons - ons]]
    try:
        _, p_val, _, _ = chi2_contingency(observed)
        if p_val < 0.05:
            chi_biased.append((vid, p_val))
    except:
        continue

for vid, p in sorted(chi_biased, key=lambda x: x[1]):
    print(f"Vehicle {vid} → p = {p:.6f}")
