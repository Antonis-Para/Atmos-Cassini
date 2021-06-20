#dataset used: https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-forecasts?tab=form

import cdsapi
import matplotlib.pyplot as plt # import libraries
import pandas as pd # import libraries
import netCDF4 # import libraries

class bcolors:
    HEADER 		= '\033[95m'
    BLUE 		= '\033[94m'
    CYAN 		= '\033[96m'
    GREEN 		= '\033[92m'
    YELLOW 		= '\033[93m'
    RED 		= '\033[91m'
    ENDC 		= '\033[0m'
    BOLD 		= '\033[1m'
    UNDERLINE		= '\033[4m'

###INPUT FROM USER###
_area = [35.35, 25.1, 35.3, 25.2]
_time = [
            '00:00', '04:00', '08:00',
            '12:00', '16:00', '20:00',
        ]
### ###


filename = 'download.nc'

#Get results from database
c = cdsapi.Client()
c.retrieve(
    'cams-europe-air-quality-forecasts',
    {
        'model': 'ensemble',
        'date': '2021-06-17/2021-06-19',
        'format': 'netcdf',
        'area': _area,
        'leadtime_hour': '0',
        'time': _time,
        'type': 'analysis',
        'level': [
            '0', '250', '50',
        ],
        'variable': [
            'carbon_monoxide'
        ],
    },
    filename)
	
nc = netCDF4.Dataset(filename) 

#Will print the carbon levels with different colours
def print_carbon(str, var):
	if (var < 110) : print(str, bcolors.GREEN, var, bcolors.ENDC)
	elif (var < 135) : print(str, bcolors.YELLOW, var, bcolors.ENDC)
	else : print(str, bcolors.RED, var, bcolors.ENDC)

iter = 0
for time in nc['co_conc']: #for every given our from the start date till the end date
	print("Time: ", _time[iter % len(_time)])
	print_carbon("Carbon monoxide at 0m:   " , time[0][0][0]) #x,y is 0,0 for now. we look into one cube
	print_carbon("Carbon monoxide at 50m:  " , time[1][0][0])
	print_carbon("Carbon monoxide at 250m: " , time[2][0][0])
	iter = iter + 1;
