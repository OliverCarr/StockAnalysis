'''
This programme was designed to take the raw data from scandi.csv 
and sort it so that it is simpler to explor and understand.
'''
import pandas as pd
import numpy as np
import time
from csv import writer

start = time.time() #Keeping track of time for varrious 


#Reading the raw data into a dataframe
filename = 'scandi.csv'
names = ['Stock', 'ID', 'Bid$', 'Ask$', 'Trade$', 'BidV', 'AskV', 'TradeV', 'Update', '_', 'Date', 'Time', 'Opening$', '__', 'Condition', '___']
data = pd.read_csv(filename, names=names)
print(time.time()-start)


#These were used to prduces a list of unique stock names
'''
array = data.values
stock = array[:,0]
clean = np.unique(stock)
'''
#       DataShape = (13260277, 16)


#Sorting the data for easeof use. By:
#1. Name of Stock
#2. Date
#3. Time
start = time.time()
sorted_df = data.sort_values(by=['Stock','Date','Time'])
print(sorted_df)
print(time.time()-start)

#Push the sorted dataframe into a csv
sorted_df.to_csv('Sorted.csv', header=None, index=None)
print(time.time()-start)
