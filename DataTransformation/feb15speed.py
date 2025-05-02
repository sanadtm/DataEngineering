import pandas as pd

# read necessary Column
df = pd.read_csv('bc_veh4223_230215.csv', usecols=['VEHICLE_ID', 'METERS', 'OPD_DATE', 'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'])
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y:%H:%M:%S')
df['TIMESTAMP'] = df['OPD_DATE'] + pd.to_timedelta(df['ACT_TIME'], unit='s')
df = df[df['VEHICLE_ID'] == 4223]
speed = [0]

# loop through and calculate speed
for i in range(1, len(df)):
    meter = df['METERS'].iloc[i] - df['METERS'].iloc[i-1]
    time = (df['TIMESTAMP'].iloc[i] - df['TIMESTAMP'].iloc[i-1]).total_seconds()
    if time != 0:
        speed.append(meter / time)
    else:
        speed.append(0)

df['SPEED'] = speed
max_row = df.loc[df['SPEED'].idxmax()]
print(max_row)