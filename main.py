from p_acquisition import m_acquisition as macq
from p_wrangling import m_wrangling as mw
from p_reporting import m_reporting as mr

import argparse

import warnings


warnings.simplefilter(action='ignore')

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', help= " '-a all' (Get the closest bike station for all consulates and embassies in Madrid)\n '-a select' (Select a set of bike stations from Madrid's database) ")
parser.add_argument('-c', '--singleConsulate', help= " Get the closest bike station to the consulate inputted\n Example: '-c Perú")
parser.add_argument('-e', '--singleEmbassy', help= " Get the closest bike station to the embassy inputted\n Example: '-e Estados Unidos de América' ")

args = parser.parse_args()
variables = vars(args)

url_embas = 'https://datos.madrid.es/egob/catalogo/201000-0-embajadas-consulados.csv' #Embassy and consulate database url
url_bikes = './data/CSV_imports/bicimad.csv'                                          #BiciMad downloaded database

raw_dframes = macq.acquire(url_embas, url_bikes)                                      #Acquire in order to get both databases and turn them into dframes
selec_dframes = mw.dframe_col_selector(raw_dframes[0], raw_dframes[1])                #Dframes columns are selected

mr.user_prompt(selec_dframes, variables)

























