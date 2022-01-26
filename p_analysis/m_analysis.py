from p_wrangling import m_wrangling as mw
import pandas as pd
from fuzzywuzzy import fuzz
pd.set_option("display.max_rows", None, "display.max_columns", None)

#calculates distances and returns list of them
def distance_calculator (df, lat, long):    
    distances_list = []
    for i in range(len(df)):   
        distance = mw.distance_meters(lat,long , df['LATITUDE'][i], df['LONGITUDE'][i])
        distances_list.append(float(distance))
        
    return distances_list

def closer_finder (localizacion_id, emba_dframe, bike_dframe):
    long = emba_dframe['LONGITUD'][localizacion_id]
    lat = emba_dframe['LATITUD'][localizacion_id]
    
    if long != long or lat != lat:
        return emba_dframe.iloc[localizacion_id]
    
    else:
        results = mw.dframe_chopper(long, lat, bike_dframe, 0)
        result_df = results[0]
        times = results[1]
        result_df = result_df.reset_index()
        result_df['distances'] = distance_calculator(result_df, lat, long)
        if len(result_df[result_df.distances < (278.680968) * (times)]) == 0:            
            results = mw.dframe_chopper(long, lat, bike_dframe, (times + 1))
            result_df = results[0]
            times = results[1]
            result_df = result_df.reset_index()
            result_df['distances'] = distance_calculator(result_df, lat, long)
            return (result_df.sort_values(by='distances', ascending=True).head(1))    
        else:
            return (result_df.sort_values(by='distances', ascending=True).head(1)) 
#Looks for coincidence between inputted country and actual database's embassy or consulate
def emba_consu_finder (inputted_place, tkn, selec_dframes, threshold):
    results_dframe = pd.DataFrame()
    ind_list = []
    name = []
    ratio = []
    
    for i in range(len(selec_dframes[0]['NOMBRE'])):
        if selec_dframes[0]['NOMBRE'][i][0] == tkn:
            x = fuzz.token_sort_ratio(inputted_place, selec_dframes[0]['NOMBRE'][i].split("de")[1])

            if x > threshold:
                ratio.append(x)
                name.append(selec_dframes[0]['NOMBRE'][i])
                ind_list.append(i)

        elif tkn == "X":
            x = fuzz.token_sort_ratio(inputted_place, selec_dframes[0]['NOMBRE'][i].split("de")[1])

            if x > threshold:
                ratio.append(x)
                name.append(selec_dframes[0]['NOMBRE'][i])
                ind_list.append(i)

    results_dframe['ind'] = ind_list
    results_dframe['ratio'] = ratio
    results_dframe['name'] = name
    
    return results_dframe
#Sorts dataframe to select top option
def emba_consu_final_pick (inputted_place, tkn, selec_dframes):

    results_dframe = emba_consu_finder (inputted_place, tkn, selec_dframes, 80)
    if results_dframe.empty:       
        return results_dframe
    
    elif results_dframe.empty == False:    
        return results_dframe.sort_values(by="ratio", ascending=False).head(1)
#Function prints closest bike station to the user while returning coordinates from both places
def question_answer (tkn, arg_1, selec_dframes):
    guess = emba_consu_final_pick(arg_1, tkn, selec_dframes)

    if guess.empty:                    
        print("\n **We couldn't find the place you are looking for. Please, try again\n")
        exit()

    else:
        place = ''.join(list(guess['name']))

    
    x = input("\n **Are you looking for the closest bike station to " + place + "?\n\n y/n: ")
    if x == "y":

        index_place = list(guess['ind'])[0]
        stlat = selec_dframes[0]['LATITUD'][index_place]
        stlon = selec_dframes[0]['LONGITUD'][index_place]
        station_info = closer_finder(index_place, selec_dframes[0], selec_dframes[1])
        endlat = station_info['LATITUDE'][0]
        endlon = station_info['LONGITUDE'][0]
        address = list(station_info['address'])[0]
        station_name = list(station_info['name'])[0]
        distance_aprox = int(list(station_info['distances'])[0])
        
        print("\n **The closest station to " + place + " is " + station_name + ".\n Address: " + address +". At aprox. " + str(distance_aprox) + " meters. \n")
        return (stlat, stlon, endlat, endlon)

    else:
        inp = input("\n **Please enter correct  name or press 'e' to exit program:\n\n:")
        if inp == "e":
            exit()

        else:
            question_answer(tkn, inp, selec_dframes )
#Used in '-a select' to ask question during while loop
def select_question_maker ():
    brk = False
    inp = input("\n ===> ")
    if inp == "":
        brk = True
    return (inp, brk)



    