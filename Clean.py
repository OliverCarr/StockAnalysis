'''
This programme was made to clean the data and prepare it for later analysis. 
'''

#Instructions from email for reference 
'''
Please also exclude auctions from your analysis. 
There should be c. 2 auctions a day - morning and afternoon. 
During this period you will see crossed spreads (i.e. bid price is larger than ask price) along with specific condition codes
Please only include the XT condition code (along with no condition code).
'''
import pandas as pd
import numpy as np
import time
from csv import writer

start = time.time()

#Pulling in the sorted csv 
filename = 'Sorted.csv'
names = ['Stock', 'ID', 'BidP', 'AskP', 'TradeP', 'BidV', 'AskV', 'TradeV', 'Update', '_', 'Date', 'Time', 'OpeningP', '__', 'Condition', '___']
df = pd.read_csv(filename, names=names)

#Filling the empty cells in the condition column
df['Condition'].fillna('BLANK', inplace  = True)

#Adding new columns to the dataframe to use in analysis

#Time difference between trades
df['TimeSinceTrade'] = df['Time'].diff()
#Creating a column to track the changes in trade price
df['Tick'] = df['TradeP'].diff()
#making note of the time at wich the trade price changed from one price to another 
df.loc[df['Tick'] == 0, 'Ticktime'] = 0
df.loc[df['Tick'] != 0, 'Ticktime'] = df['Time']

#Calculating the spread for each trade
df['Spread'] = df['AskP'] - df['BidP']
#Calculating the trade value of each trade
df['TradeValue'] = df['TradeP']*df['TradeV']


#Removing all trades with negative spreads -- Auctions
index =df[df['Spread'] < 0].index
df.drop(index, inplace=True)

#Removing all trades that do not meet the conditional requirements 
#Adding a column called 'Keep' to track all condition
df.loc[(df['Condition'] == 'BLANK') | (df['Condition'] == 'XT'), 'Keep'] = 1  
df['Keep'].fillna(0, inplace=True)
index =df[df['Keep'] == 0].index
df.drop(index, inplace=True)

#print(df.head(330))


#Push to new Cleaned csv
df.to_csv('Cleaned.csv', header=None, index=None)



