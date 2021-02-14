import pandas as pd
import matplotlib.pyplot as plt
import xarray as X
import numpy as np
import math
import glob
import argparse
import datetime
import math
import sys
import time
from types import SimpleNamespace



def parse_arguments():
	spat_res = 10
	output_filename = 'spire_wrfda_input.txt'
	parser = argparse.ArgumentParser(description="Need to pass arguments.")	
	parser.add_argument("--spat_res", type=int, default= spat_res, help = "Need to pass the spatial resolution")
	parser.add_argument("--output_filename", type=str, default= output_filename, help = "Need to pass the output filename")
	args = parser.parse_args()
	return args.spat_res, args.output_filename



def initialize_default_variables():
	def_var=SimpleNamespace()
	def_var.dummy_float=-888888.00000
	def_var.height=def_var.dummy_float
	def_var.dp=def_var.dummy_float
	def_var.speed=def_var.dummy_float
	def_var.direc=def_var.dummy_float
	def_var.u=def_var.dummy_float
	def_var.v=def_var.dummy_float
	def_var.rh=def_var.dummy_float
	def_var.thic=def_var.dummy_float
	def_var.spacing=' '*7
	def_var.dummy=-888888.0
	def_var.id=23
	def_var.name='{:<40}'.format('Huntsville')
	def_var.platform='{:<40}'.format('FM-35 TEMP')
	def_var.source='{:>40}'.format('Spire')
	def_var.elevation=502
	def_var.num_vld_fld=1
	def_var.num_error=def_var.dummy
	def_var.num_warning=def_var.dummy
	def_var.seq_name=def_var.dummy
	def_var.num_dups=def_var.dummy
	def_var.is_sound='         T'
	def_var.bogus='         F'
	def_var.discard='         F'
	def_var.sut=def_var.dummy
	def_var.julian=def_var.dummy
	def_var.second_last='-777777.00000      0-777777.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
	def_var.last='     17      0      0'
	return def_var





def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Function to display a progress bar
            printProgressBar(
                i + 1, lon.shape[0]-1, prefix = 'Calculating DESIS swath coordinates:', suffix = 'Complete ', length = 70)
        Parameters:
            iteration: Current iteration value
            total: Total iteration value
            prefix: Prefix text
            suffix: Suffix Text
            decimals: Number of decimals to be printed while displaying the progress percentage
            length: Percentage of screen covering the progress bar
            fill: Fill character value in the progress bar
            printEnd: Ending character. Eg. "\r"
        Returns:
            None
    """

    # calculate percentage in 2 decimal places
    percent = 100 * (iteration / float(total))
    percent = f'{percent:.{2}f}'

    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    if iteration == total:
        print()


def write_header_and_data(output_data):
	def_vals=initialize_default_variables()
	for distance_index in range(0,np.int(distan[-1]),spatial_res):
		indices=np.where(np.logical_and(distan>distance_index , distan<distance_index+10))
		indices=indices[0]
		header=('%20.5f%20.5f%40.0f%s%s%s%20.5f%10.0f%10.0f%10.0f%10.0f%10.0f%s%s%s%10.0f%10.0f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s' %(np.nanmean(latitude[indices]),np.nanmean(longitude[indices]),def_vals.id,def_vals.name,def_vals.platform,def_vals.source,def_vals.elevation,def_vals.num_vld_fld,def_vals.num_error,def_vals.num_warning,def_vals.seq_name,def_vals.num_dups,def_vals.is_sound,def_vals.bogus,def_vals.discard,def_vals.sut,def_vals.julian,datechar,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing,def_vals.dummy,def_vals.spacing))
		output_data.append([header])
		for index in range(0,indices.shape[0]-1):
			lat=latitude[indices[index]]
			lon=longitude[indices[index]]
			pres=pressure[indices[index]]
			temp=temperature[indices[index]]
			out=('%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s%13.5f%s' %(pres,def_vals.spacing,def_vals.height,def_vals.spacing,temp,def_vals.spacing,def_vals.dp,def_vals.spacing,def_vals.speed,def_vals.spacing,def_vals.direc,def_vals.spacing,def_vals.u,def_vals.spacing,def_vals.v,def_vals.spacing,def_vals.rh,def_vals.spacing,def_vals.thic,def_vals.spacing))
			data=[out]
			output_data.append(data)
		output_data.append([def_vals.second_last])
		output_data.append([def_vals.last])
	return output_data



def write_data_in_file(output_data,output_filename):
	with open(output_filename, 'w') as f:
        	for item1 in output_data:
                	for item in item1:
                        	f.write("%s\n" % item)



if __name__ == "__main__":
	spatial_res, output_filename = parse_arguments()
	output_data=[]
	mylist = [f for f in glob.glob("*.nc")]
	A=X.open_dataset(mylist[0])
	timestamp=A.attrs['processing_timestamp']
	datestamp=str(int(''.join(filter(str.isdigit, timestamp))))[:10]
	datechar='      ' + datestamp +'0000'
	sequence = 0
	for filelist in mylist:
		print(filelist)
		printProgressBar( sequence + 1, len(mylist), prefix='Retrieving location:', suffix='Complete ', length=70)
		sequence = sequence + 1
		filename=filelist
		A=X.open_dataset(filename)
		latitude=A['Lat']
		longitude=A['Lon']
		temperature=A['Temp']
		pressure=A['Pres']*100
	
		start=np.array([longitude[0],latitude[0]])
		distan=[]
		for index in range(0,latitude.shape[0]-1):
			lat=latitude[index]
			lon=longitude[index]
			second=np.array([lon,lat])
			distan.append(np.sqrt( (start[0] - second[0])**2 + (start[1] - second[1])**2 )*111.11)
		distan=np.array(distan)
		output_data=write_header_and_data(output_data)	
	
	write_data_in_file(output_data,output_filename)


