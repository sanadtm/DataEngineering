import pandas as pd
# read necessary Column
df = pd.read_csv('bc_trip259172515_230215.csv', usecols=['METERS', 'OPD_DATE', 'ACT_TIME'])
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y:%H:%M:%S')
df['TIMESTAMP'] = df['OPD_DATE'] + pd.to_timedelta(df['ACT_TIME'], unit='s')
speed = [0] 

# loop through and calculate speed
for i in range(1, len(df)):
    meter = df.loc[i, 'METERS'] - df.loc[i - 1, 'METERS']
    time = (df.loc[i, 'TIMESTAMP'] - df.loc[i - 1, 'TIMESTAMP']).total_seconds()
    if time != 0:
        speed.append(meter / time)
    else:
        speed.append(0)
df['SPEED'] = speed
# print(df['SPEED'])
print("Min:", df['SPEED'].min(),"| Max:", df['SPEED'].max()," | Avg:", df['SPEED'].mean() )
