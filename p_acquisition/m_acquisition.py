import requests 
import pandas as pd
from io import StringIO

def acquire (url_embas, url_bikes):
    #First csv import from API (Embassies and consulates)
    response = (requests.get(url_embas)).text
    embassy_dframe = pd.read_csv(StringIO(response), delimiter=";")
    #Second import from repo's data (BiciMad)
    bikes_dframe = pd.read_csv(url_bikes)   

    return (embassy_dframe, bikes_dframe)