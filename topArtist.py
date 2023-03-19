import pandas as pd
import matplotlib.pyplot as plt
import plotting
import numpy as np

def top_artist(data: pd.DataFrame, 
               topNumber: int, 
               year: int, 
               artistColumn: str = 'master_metadata_album_artist_name' , 
               yearColumn: str = 'whichYear', 
               timeColumn: str = 'ms_played') -> list[str]:
        
        temp = data[(data[artistColumn] != 'Unknown Artist') & (data[yearColumn] == year)]
        
        return list(temp.groupby(artistColumn).sum().sort_values(by=timeColumn, ascending=False).head(topNumber).index)

## Grab the top 5 of each year to include as faint grey lines, removing most recent year (as likely to only be partial)
def artist_list(data: pd.DataFrame, 
                topNumber: int,
                combine: bool,
                yearColumn: str = 'whichYear') -> set[str]:
    a = []
    ## Removing unknown artists in the data from importing files manually into spotify
    for y in range(data[yearColumn].min(), data[yearColumn].max()):
        temp = data[data[yearColumn] == y]
        d = top_artist(data, topNumber, y)
        
        if combine == True:
            a.extend(d)
        else:
            a.append(d)
    
    if combine == True:
        return set(a)
    else:
        return a

## Grab a time series of each month and year in the dataset
def dates_list(data: pd.DataFrame, yearColumn: str = 'whichYear') -> list[list[int]]:
    mons = []
    yrs = []
    for y in range(data[yearColumn].min(), data[yearColumn].max()):
        for m in range(1,13):
            mons.append(m)
            yrs.append(y)
    return [mons, yrs]

def artist_play(data: pd.DataFrame, 
                artistColumn: str = 'master_metadata_album_artist_name',
                yearColumn: str = 'whichYear',
                monthColumn: str = 'whichMonth',
                timeColumn: str = 'ms_played'
                ) -> pd.DataFrame:

    d = pd.DataFrame(dates_list(data)).T
    d.columns=['Months', "Years"]

    ## Get monthly timeseries play time for each top artist
    for a in artist_list(data, 5, True):
        temp = data[data[artistColumn] == a].groupby([yearColumn, monthColumn]).sum().copy()
        temp = temp.reset_index()
        temp = temp[[monthColumn, yearColumn, timeColumn]].copy()
        temp.columns = ["Months", "Years", a]
        d = d.merge(temp, left_on=['Months', 'Years'], right_on=['Months', 'Years'], how='left')

    ## Add time to index and remove Date Columns
    d.index = (d.index / 12 + d['Years'].min()) + (1/12)
    for c in ['Months', "Years"]:
        d.drop(c, inplace=True, axis=1)

    ## Convert to cumulative hours
    d = d.fillna(0).cumsum()
    d = (d*0.001)/60/60

    return d

def artist_plot(data: pd.DataFrame, yearColumn: str = 'whichYear') -> list[plt.figure, plt.axes]:
    ## General Plotting
    fig,ax = plotting.gen_plot()
    plotting.set_label(x=None, y='Hours', title=None)
    plotting.set_axis(x=[data[yearColumn].min(),yearColumn.max()],y=[0,1.01])
    plt.yticks(np.linspace(0,1,6), [int(x) for x in np.linspace(0,plotting.assumption['max_value_x'],6)])

    ## Data
    backgroundArtist = artist_list(data, 25, False)
    foregroundArtist = artist_play(data)
    ## Set to [0,1] for easy text positioning
    foregroundArtist = foregroundArtist / plotting.assumption['max_value_x']

    ## Text Background
    for yearIndex, years in enumerate(backgroundArtist):
        for artistIndex, artist in enumerate(years):
            plt.text(2017+yearIndex+0.5, 
                     .99-(artistIndex/25), 
                     artist, 
                     color='grey', va="top", ha="center", size=plotting.assumption['text_size'], alpha=0.3-(0.25/30)*artistIndex)
    
    ## Line Foreground
    va_loc = ['center']*5 ## Pass differnt va commands in loop if values are too similar and overlap
    for i, a in enumerate(foregroundArtist.T.sort_values(foregroundArtist.T.columns[-1], ascending=False).index):
        if i < 5:
            plt.plot(foregroundArtist[a], c=plotting.colrs['green'])
            plt.text(list(foregroundArtist.index)[-1], foregroundArtist[a].iloc[-1], a, c="white", va=va_loc[i], size=plotting.assumption['text_size']) 
        else:
            plt.plot(foregroundArtist[a],  c=plotting.colrs['grey_super_trans'], lw=2)

    return fig, ax

