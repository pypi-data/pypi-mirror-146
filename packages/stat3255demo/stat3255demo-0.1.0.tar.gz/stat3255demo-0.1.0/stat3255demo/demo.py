# +
import pandas as pd

def nyc_open_data():
    
    data = pd.read_csv("https://raw.githubusercontent.com/statds/ids-s22/0b4ae79e494ed9c33e3fb8900a9145de76cd97ed/notes/data/nyc_mv_collisions_202201.csv")
    
    return(data)
