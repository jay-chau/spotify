import os
import pandas as pd
import pytz

## Loops through a folder and imports all JSON files within. Personal Data available to download from Spotify User Settings.
def read_raw(folder: str = 'rawData', timeZone: str = 'UTC', dateColumn: str = 'ts') -> pd.DataFrame:
    data = pd.DataFrame()
    for file in os.listdir(folder):
        try:
            temp = pd.read_json(f"{folder}\{file}", orient="columns")

            ## Convert Time from UTC to local
            temp[dateColumn] = pd.to_datetime(temp[dateColumn], utc=True).dt.tz_convert(pytz.timezone(timeZone))

            data = pd.concat([data, temp])
        except:
            print(f"Issue reading file {file}")
    return data

## Create additional variables for charts and analysis
def summary_calc(data: pd.DataFrame, dateColumn: str = 'ts', timeColumn: str = 'ms_played', playThreshold: int = 30000) -> pd.DataFrame:
    temp = data.copy()
        
        ## Current Time
    temp['whichHour'] = [x.hour for x in temp[dateColumn]]
    temp['whichWeekday'] = [x.dayofweek for x in temp[dateColumn]]
    temp['whichMonth'] = [x.month for x in temp[dateColumn]]
    temp['whichYear'] = [x.year for x in temp[dateColumn]]

        ## Check if song is counted as "played"
    temp['played'] = temp[timeColumn] > playThreshold

    return temp

## Replace artists who are the same but have different accounts
def replace_artist(data: pd.DataFrame, artistColumn: str = 'master_metadata_album_artist_name') -> pd.DataFrame:
    for artist, replacement in zip(['Tech N9ne Collabos'], ['Tech N9ne']):
        data[artistColumn] = data[artistColumn].replace(artist, replacement)
    return data

def process() -> pd.DataFrame:
    d = summary_calc(read_raw())
    d = replace_artist(d)
    d.to_hdf('spotifyData.h5', key='data', mode='w')
    return d