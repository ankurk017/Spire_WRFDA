# spire_to_wrf

## Description
User can create a file having the spire data in a specific format so that it can be ingested into The Weather Research and Forecasting Data Assimilation (WRFDA) as an input to the obsproc (an executable in WRFDA).

## Required Libraries
sys, pandas, xarray, numpy, math, glob, argparse, datetime, math, time, SimpleNamespace

## Arguments
This tool needs 2 optional arguments as follows,

1. _spat_res_: Spatial Resolution of the simulation (in km). Default value of this argument is 10km, and it will be considered if the user does not provide this optional argument.

2. _output_filename_: Filename of the output text file. Default value of this argument is _spire_wrfda_input.txt_.


## Examples

1. User needs to specify spat_res, end_date and _output_filename_ as arguments

`$python spire_to_wrf.py  --spat_res=15 --output_filename='spire_wrfda_input.txt`

`$ python spire_to_wrf.py  --spat_res=15`


2. User can chose not to provide any arguments. If not provided, program will automatically take 10 km as the _spat_res_, and _spire_wrfda_input.txt_ as output_filename
`$python  spire_to_wrf.py`


