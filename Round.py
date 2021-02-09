'''
This programme examines the data created by divide and prduces a csv file describing the round number effect
'''

import pandas as pd
import numpy as np
import time
from csv import writer

start = time.time()


#This function takes the file name and returns a two vales as a list 
#The first is the percentage of trade volumes for that stock that end in a zero
#The second is the percentage of trade values for that stock that end in a zero
def ZeroPercents(filename):
    #Pulls in the selected file
    print(filename)
    names = ['Stock', 'ID', 'BidP', 'AskP', 'TradeP', 'BidV', 'AskV', 'TradeV', 'Update', '_', 'Date', 'Time', 'OpeningP', '__', 'Condition', '___', 'TimeSinceTrade','Tick','Ticktime', 'Spread', 'TradeValue', 'Keep' ]
    df = pd.read_csv(filename, names=names)


    #Creatues two new columns that contain the last digit of each trade volume and trade value
    #by converting the values to strings and striping all but the last one
    df['LastDigitVol'] = df['TradeV'].astype(str).str.strip().str[-1]
    df['LastDigitVal'] = df['TradeValue'].astype(str).str.strip().str[-1]

    #Finds the length of the dataframe 
    L = df.shape[0]

    #Clears variables for next loop
    a=0
    b=0

    #Loops throught the dataframe counting zeros by incrementing a and b
    for i in range(L):
        if df.loc[i,'LastDigitVol']=='0':
            a += 1
        if df.loc[i,'LastDigitVal']=='0':
            b += 1

    #Calculated as a percentage
    VolPercent = 100*a/L
    ValPercent = 100*b/L

    #print('Trade Volume is ', VolPercent,'%',' round numbers' ) 
    #print('Trade Value is ', ValPercent,'%',' round numbers' )
    
    #returns results as list
    return [VolPercent, ValPercent]


#Pulling in file names 
filename = 'FirstPass/STOCKS.csv'
names = ['Stock']
df_st = pd.read_csv(filename, names=names)
print('The names of each stock')
print(df_st)
array = df_st['Stock'].values.tolist()

#Creating empty array to fill with results
perc = np.zeros((100,2))



#Loops through the 100 files of stocks
for i in range(100):
    print(i, 'of 99 Stocks' )
    name = df_st.loc[i, 'Stock']
    print(name)
    if name == 'BBHBEAT Index': #With the exeption of one
        continue

    #Executes function defined above and fills up empty array
    filename = 'stocks/%s.csv' % name
    perc[i,:] = ZeroPercents(filename)




#Converts results array into dataframe and push to csv file 
DF = pd.DataFrame(perc, index = array, columns=['TradeVolume','TradeValue'])
DF.to_csv('RoundNumbers.csv')

'''Some values for all stocks -- found in early itterations'''
#Trade Volume is 26.62025964554602 % round numbers
#Trade Value is 37.17116456631621 % round numbers

#shape = df.shape
#print(shape)


print('Done')