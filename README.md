# Where's the closest BiciMad station?  
This pipeline will find the closest BiciMad station to a given set of embassies and consulates within Madrid  
Status: working on refactoring

## Technology Stack
* Python (3.7)
* Pandas
* Requests
* GeoPandas
* FuzzyWuzzy
* PIL / Pillow
* Argparse

## How does it work?
This program will first download csv's from Ayuntamiento de Madrid's database.  
Then it will find the closest BiciMad station to the specified embassy/consulate (or a set of them) and return the answer in terminal (for singular place of interest) or in csv format (for a set of places).    
  
It will achieve this by calculating the distances between given coordinates using geopandas modules.  
In order to maximize efficiency, the program will 'chop' or 'slice' the dataframe before calculating distances. It will 'generate a squared area' with the place of interest right in the center, removing all of the stations that fall outside of said area. This is calculated adding and substracting a constant number to both longitude and latitude of the picked embassy/consulate's coordinates, thus generating four straigth lines that will form the square: 

(imagen 1)

Once the square is built and the dataframe is reduced to a small set of possible BiciMad stations, the code will then pick the constant we talked about earlier as the radius of a circle that will make sure we are finding the actual closest station to the place of interest.  
The number of this constant can be easily changed within the code in order to find some sort of 'sweet spot' in terms of speed. If the code can't find a station within the circle, it will enlarge the radius, it will form the square and circle again, and it will repeat the process until the loop breaks. 

(imagen 2)

 ### The command line
 The code allows four different arguments:  
 First two involve the search for a BiciMad station close to one consulate or embassy:  
 
  We use -c (for consulates)  
   
 `python main.py -c argentina`  
   
 or -e (for embassies)  
   
 `python main.py -e rusia`  
 
 The program allows the selection of a given set of places, to run this, type:  
   
 `python main.py -a select`
 
 ![alt text](https://github.com/HAL9044/IronHack_Module1_Project/blob/main/images/imagen%201(1).jpg)
 
 Finally, you can get a csv with all of the closest station for every single consulate and embassy in Madrid:  
 
 `python main.py -a all`  
 
 The last two options will export a csv file inside the data/CSV_exports folder.   
 The first two, on the other hand, will only export a map with the specified destinations.
   

## Folder structure
(imagen 3)

## TODO
Code is currently being refactored
