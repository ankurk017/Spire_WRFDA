import pandas as pd


import matplotlib.pyplot as plt
import numpy as np
import math
import glob
import xarray as X

output_data=[]
height=-888888.00000
dp=-888888.00000
speed=-888888.00000
direc=-888888.00000
u=-888888.00000
v=-888888.00000
rh=-888888.00000
thic=-888888.00000
spacing=' '*7
dummy=-888888.0
id=23
name='{:<40}'.format('Huntsville')
platform='{:<40}'.format('FM-35 TEMP')
source='{:>40}'.format('Spire')
elevation=502
num_vld_fld=1
num_error=dummy
num_warning=dummy
seq_name=dummy
num_dups=dummy
is_sound='         T'
bogus='         F'
discard='         F'
sut=dummy
julian=dummy

datechar='      20200820000000'
mylist = [f for f in glob.glob("*.nc")]
print(mylist)
for filelist in mylist:
	print(filelist)
	filename=filelist
	A=X.open_dataset(filename)
	latitude=A['Lat']
	longitude=A['Lon']
	temperature=A['Temp']
	pressure=A['Pres']*100
	print(pressure.shape)

	start=np.array([longitude[0],latitude[0]])
	print(start)
	distan=[]
	for index in range(0,latitude.shape[0]-1):
		lat=latitude[index]
		lon=longitude[index]
		second=np.array([lon,lat])
		distan.append(np.sqrt( (start[0] - second[0])**2 + (start[1] - second[1])**2 )*111.11)
	distan=np.array(distan)
	final_output=[]	
	for distance_index in range(0,50,10):
		print(distance_index)
		indices=np.where(np.logical_and(distan>distance_index , distan<distance_index+10))
		indices=indices[0]
		print(indices)
		header=('%20.5f%20.5f%40.0f%s%s%s%20.5f%10.0f%10.0f%10.0f%10.0f%10.0f%s%s%s%10.0f%10.0f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s' %(np.nanmean(latitude[indices]),np.nanmean(longitude[indices]),id,name,platform,source,elevation,num_vld_fld,num_error,num_warning,seq_name,num_dups,is_sound,bogus,discard,sut,julian,datechar,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing,dummy,spacing))
		output_data=[]
		output_data.append([header])
		for index in range(0,indices.shape[0]-1):
			lat=latitude[indices[index]]
			lon=longitude[indices[index]]
			pres=pressure[indices[index]]
			temp=temperature[indices[index]]
			out=('%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s' %(pres,spacing,height,spacing,temp,spacing,dp,spacing,speed,spacing,direc,spacing,u,spacing,v,spacing,rh,spacing,thic,spacing))
			data=[out]
			output_data.append(data)
		finaloutput=output_data
		final_output.append(finaloutput)
	jio



with open('spire_output.txt', 'w') as f:
        for item1 in output_data:
                for item in item1:
                        f.write("%s\n" % item)


#	data = [header,out,last3,last2,last1]
#	output_data.append(data)
#outputdata=np.concatenate(output_data).tolist()

