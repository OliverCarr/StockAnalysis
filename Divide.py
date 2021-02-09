'''
This one is here to divide the stocks into 100 seperate csv file
This was done to easily seperate each stock from its alphabetical neighbours for analysis
'''
import pandas as pd
import numpy as np
import time
from csv import writer

start = time.time()

#Bring in the cleaned and prepared data
filename = 'Cleaned.csv'
names = ['Stock', 'ID', 'BidP', 'AskP', 'TradeP', 'BidV', 'AskV', 'TradeV', 'Update', '_', 'Date', 'Time', 'OpeningP', '__', 'Condition', '___', 'TimeSinceTrade','Tick','Ticktime', 'Spread', 'TradeValue', 'Keep' ]#expanded list 
df = pd.read_csv(filename, names=names)
#print(df.head())



#Reading a dataframe with the names of all the stocks
filename = 'FirstPass/STOCKS.csv'
names = ['Stock']
df_st = pd.read_csv(filename, names=names)
#print('The names of each stock')
#print(df_st)



#shape = df.shape
#print(shape)  #--> (13009813, 16)


#This loop cycles through the cleaned data and breaks them into 100 individual csv files
#Lots of commented out print statments for keeping track of progress
for i in range(100):
    #print(i, 'Out of 99')

    name =  df_st.loc[i, 'Stock'] #Pulls the stock names into a one dimentional list
    #print(name)


    #clear the variable from the last loop  
    new = 0 

    #print("selecting the '%s' stocks" % name)

    #Select the particular stocks from the dataframe
    new = df.loc[df['Stock'].isin([name])]

    #print(" outputing the header of the selection")
    #print(new.head())

    #print("Pushing to CSV")
    new.to_csv('stocks/%s.csv' % name, header=None, index=None) #Using %s to insert new file names

print("Done")

