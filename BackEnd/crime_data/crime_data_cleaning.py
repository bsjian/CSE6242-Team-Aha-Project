import numpy as np
import pandas



file_1 = pandas.read_csv("COBRA-2009-2017.csv", error_bad_lines=False)
file_2 = pandas.read_csv("Cobra-2018.csv", error_bad_lines=False)
#data = pandas.merge(file_1, file_2, on=['Report Number', 'Report Date', 'Location'\
#, 'UCR Literal', 'UCR #', 'Neighborhood', 'Latitude', 'Longitude'], how='left') add cols
data = pandas.concat([file_1, file_2],axis=0) #add rows
ucr_code = set(data['UCR #'])
ucr_literal = set(data['UCR Literal'])
clean_col_data = data[['Report Number', 'Report Date', 'Location'\
, 'UCR Literal', 'Latitude', 'Longitude']]
clean_col_data.dropna(axis=0, how='any', inplace=True)
#print(ucr_literal)
#{'BURGLARY-RESIDENCE', 'BURGLARY-NONRES', 
# 'AUTO THEFT', 'ROBBERY-PEDESTRIAN', 
# 'MANSLAUGHTER', 'ROBBERY-COMMERCIAL', 
# 'HOMICIDE', 'LARCENY-NON VEHICLE', 
# 'AGG ASSAULT', 'LARCENY-FROM VEHICLE', 
# 'ROBBERY-RESIDENCE'}
clean_col_data.to_csv(r'crime_data.csv', encoding='gbk')