import pandas as pd
import requests

from PIL import Image
from io import BytesIO

from p_analysis import m_analysis as ma

#Generates final dataframe when 
def final_dframe_generator (emba_dframe, bike_dframe):
    final_dframe = pd.DataFrame()
    for y in range(len(emba_dframe)):
        final_dframe = final_dframe.append(ma.closer_finder(y, emba_dframe, bike_dframe))

    final_dframe = final_dframe.reset_index()
    final_dframe = final_dframe[['name', 'address', 'LATITUDE','LONGITUDE', 'distances']]
    final_dframe['EMBACONSU'] = emba_dframe['NOMBRE']
    final_dframe.sort_values(by='distances')
    final_dframe.to_csv("./data/final_dframe.csv")
    return final_dframe
#Generates API url and returns response as image (MAP)
def route_img_generator (stlon, stlat , endlon, endlat):
    stlon = str(stlon)
    stlat = str(stlat)
    endlon = str(endlon)
    endlat = str(endlat)
    KEY = 'mO7e1GlQzPaCQnj6j0zBD2ajNtUFIvMA'
    img = requests.get("https://open.mapquestapi.com/staticmap/v4/getmap?key=" + KEY + "&size=600,400&type=map&imagetype=png&declutter=false&shapeformat=cmp&shape=uajsFvh}qMlJsK??zKfQ??tk@urAbaEyiC??y]{|AaPsoDa~@wjEhUwaDaM{y@??t~@yY??DX&scenter=" + stlat + "," + stlon + "&ecenter=" + endlat + "," + endlon)
    return Image.open(BytesIO(img.content))
    
def user_prompt (selec_dframes, variables):
    for arg in variables.items(): 

        if arg[1] != None:
            arg_0 = arg[0]
            arg_1 = arg[1]

            if arg_0 == "singleConsulate":                                            #Comparing argparse arguments in order to execute desired function
                tkn = "C"                                                             #This token is used to accelerate the search for place of interest (Consulate)
                coor = ma.question_answer(tkn, arg_1, selec_dframes)                  #Function prints closest bike station to the user while returning coordinates from both places
                image = route_img_generator(coor[1], coor[0], coor[3], coor[2])    #Coordinates are used to plot data into map
                image.save("../data/CSV_exports/route.png")   #image is saved in CSV_exports
                print("\n **An image file with the locations on a map has been saved into the CSV_exports folder in data...\n")
                          
            elif arg_0 == "singleEmbassy":                                             #This is in essence the same than above, but since tkn is E, this will look for embassies
                tkn = "E"
                coor = ma.question_answer(tkn, arg_1, selec_dframes)
                image = route_img_generator(coor[1], coor[0], coor[3], coor[2])
                image.save("../data/CSV_exports/route.png")
                print("\n **An image file with the locations on a map has been saved into the CSV_exports folder in data...\n")
                

            elif arg_0 == "all":                #looks for closest bicimad station for ALL of database's embassies or consulates
                if arg_1 == "all":
                    inp = input("\n **You are about to get the closest bike station for EVERY consulate and embassy in Madrid.\n  (CSV with results will be saved in CSV_exports within data folder) This might take a while... are you sure?\n\n y/n: ")
                    if inp == "y":

                        inp2 = input("\n **Please enter name for the final csv (No need to add '.csv' at the end): \n")
                        route = "./data/CSV_exports/" + inp2 + ".csv"
                        final_dframe = pd.DataFrame()                                                                   
                        emba_dframe = selec_dframes[0]
                        bike_dframe = selec_dframes[1]

                        for emba_consu in range(len(selec_dframes[0])):                                                 #appends closest bike station for every embassy/consulate into dframe
                            print("Calculating: " + str(emba_consu) + "/" + str(len(emba_dframe)), end='\r')
                            final_dframe = final_dframe.append(ma.closer_finder(emba_consu, emba_dframe, bike_dframe))

                        final_dframe = final_dframe.reset_index()                                           
                        final_dframe = final_dframe[['name', 'address', 'LATITUDE','LONGITUDE', 'distances']]           #Builds final dataframe
                        final_dframe['Embajada/Consulado'] = emba_dframe['NOMBRE']
                        final_dframe.sort_values(by='distances')
                        final_dframe.to_csv(route)
                        print("CSV succesfully saved in: " + route)                                                     #saves dframe

                    elif inp == "n":
                        exit()

                elif arg_1 == "select":

                    brk = False
                    places_lst = []
                    final_dframe = pd.DataFrame()
                    emba_dframe = selec_dframes[0]
                    bike_dframe = selec_dframes[1]
                    print("\n **Enter every embassy/consulate's country name you are looking for one by one. Whenever you are done, just press enter: \n")

                    while brk == False:                         #used to stop while loop
                        place = ma.select_question_maker()      #asks for embassy/consulate country's name in order to find and append to dframe
                        places_lst.append(place[0])             #when user presses enter brk == True
                        brk = place[1]
                    
                    places_lst = places_lst[:len(places_lst)-1]
                    final_lst = []                              #list of embassies and consulates index
                    names_final_lst = []                        #list of actual embassies or consulates that coincided
                    
                    for item in places_lst:
                        final_lst.append(ma.emba_consu_final_pick(item, "X", selec_dframes)['ind'][0])
                        names_final_lst.append(ma.emba_consu_final_pick(item, "X", selec_dframes)['name'][0])

                    count = 1

                    for ind in final_lst:                                               #builds final dataframe
                        print("Calculating: " + str(count) + "/" + str(len(final_lst)), end='\r')
                        final_dframe = final_dframe.append(ma.closer_finder(ind, emba_dframe, bike_dframe))
                        count+=1

                    final_dframe = final_dframe.reset_index()
                    final_dframe = final_dframe[['name', 'address', 'LATITUDE','LONGITUDE', 'distances']]
                    final_dframe['Embajada/Consulado'] = names_final_lst
                    final_dframe.sort_values(by='distances')
                    inp2 = input("\n **Please enter name for the final csv (No need to add '.csv' at the end): \n")
                    route = "../data/CSV_exports/" + inp2 + ".csv"
                    final_dframe.to_csv(route)
                    print("\n **CSV succesfully saved in: " + route)

                else:
                    print("\n **No parameter found; use '-a all' to get every station or '-a select' to make a selection from Madrid's database\n")

