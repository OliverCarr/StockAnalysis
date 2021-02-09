'''
This programme creates a new dataframe and pushes it to csv
That single csv contains all of the relevent variables that were requested for each stock
'''
import pandas as pd
import numpy as np
import time
from csv import writer
import matplotlib.pyplot as plt

start = time.time()


#Copied from Divide.py... makes a databas and list list of stocks names
filename = 'FirstPass/STOCKS.csv'
names = ['Stock']
df_st = pd.read_csv(filename, names=names)
#print('The names of each stock')
#print(df_st)
array = df_st['Stock'].values.tolist()


#some analysis needs to change based to the date
#to avoid large time jumps between trading days
date = [20150420, 20150421, 20150422, 20150423]

#Creating an empty dataframe to fill with results later 
result_header = ['Mean time between trades', 'Median time between trades', 'Longest time between trades', 'Mean time between tick changes', 'Median time between tick changes', 'Longest time between tick changes', 'Mean bid ask spread', 'Median bid ask spread' ]
results = pd.DataFrame(columns=result_header,  index= array)
#print(results)



#This loop cycles through each of the 100 files created by Divide.py
for i in range(100):
    #Stock name changes with each pass 
    print(i, 'of 99 Stocks' )
    name = df_st.loc[i, 'Stock']
    print(name)

    #The BBHBEAT Index was removed as an exception as its trades were entierly removed by the cleaning process
    if name == 'BBHBEAT Index':
        continue

    #Reads one of the divided files and creates a dataframe
    filename = 'stocks/%s.csv' % name
    names = ['Stock', 'ID', 'BidP', 'AskP', 'TradeP', 'BidV', 'AskV', 'TradeV', 'Update', '_', 'Date', 'Time', 'OpeningP', '__', 'Condition', '___', 'TimeSinceTrade','Tick','Ticktime', 'Spread', 'TradeValue', 'Keep' ]
    print("reading in the data file.......")
    df = pd.read_csv(filename, names=names)
    #print(df.head())
    #print(df.shape)


    #Creating blank arrays to fill with temporary results 
    TBT1 = np.zeros((2,4)) #Time between trades 
    TBT2 = np.zeros((2,4)) #Time between ticks
    weight1 = [0,0,0,0]
    weight2 = [0,0,0,0]


    #This loop cycles through each of the four days
    for j in range(4):
        
        #cleans out variables from privious loop
        new1 = 0
        new2 = 0

        #New dataframe with 1 day worth of data
        new1 = df.loc[df['Date'].isin([date[j]])].copy()
        #print('trades on day 1')
        
    
        #Re-applying the difference function to catch the edge cases
        new1['TimeSinceTrade'] = new1['Time'].diff()



        #Using functions to find the mean, median and maximum values of time between trades

        MEAN_tst1 = new1['TimeSinceTrade'].mean()
        #print('Mean time between trades: ', MEAN_tst1,'s')
        MEDIAN_tst1 = new1['TimeSinceTrade'].median()
        #print('Median time between trades: ', MEDIAN_tst1, 's')    
        max1 = int(new1['TimeSinceTrade'].max())
        #print('Max time between trades: ',max1,'s')

        #Filling up blank array
        TBT1[:,j] = [MEAN_tst1, max1]
        weight1[j] = new1.shape[0]

        

        #New dataframe which removes all trades where there was no change in trade value 
        new2 = new1[-new1["Ticktime"].isin(["0"])] #Removes all 0 tick times

        #Finds the time between each tick 
        new2['TimeSinceTick'] = new2['Ticktime'].diff()

        #Using functions to find the mean, median and maximum values of time between ticks


        MEAN_tst2 = new2['TimeSinceTick'].mean()
        #print('Mean time between ticks: ', MEAN_tst2,'s')
        MEDIAN_tst2 = new2['TimeSinceTick'].median()
        #print('Median time between ticks: ', MEDIAN_tst2, 's')
        max2 = int(new2['TimeSinceTick'].max())
        #print('Max time between ticks: ',max2,'s')


        #Filling up blank array
        TBT2[:,j] = [MEAN_tst2, max2]
        weight2[j] = new2.shape[0]

    #Normalise weighting results
    weight1 = np.divide(weight1,sum(weight1))
    weight2 = np.divide(weight2,sum(weight2))


    #weighting average based on number of results per day
    TBT1[0,:] = TBT1[0,:]*weight1
    TBT2[0,:] = TBT2[0,:]*weight2

    #The mean of means and the max of max values 
    tbt1_mean = np.mean(TBT1[0,:])
    tbt1_max = np.max(TBT1[1,:])

    #Median calculated for whole of stock 
    tbt1_median = df['TimeSinceTrade'].median()
    
    #The mean of means and the max of max values (ticks)
    tbt2_mean = np.mean(TBT2[:,0])
    tbt2_max = np.max(TBT2[:,1])

    #Calculating the median for tick time by removing all zero values(where price was constant)
    new = df[-df["Ticktime"].isin(["0"])] #Removes all 0 tick times
    new['TimeSinceTick'] = new['Ticktime'].diff()#Creates a new colums to compare times

    #Median calculated for whole of stock (ticks)
    tbt2_median = new['TimeSinceTick'].median()
    
    #calculating the mean and median spread for each stock
    spread_mean =  df['Spread'].mean()
    spread_median =  df['Spread'].median()


    #Arranges all of the calculated values into one row of a results database
    results.loc['%s'%name, 'Mean time between trades'] = tbt1_mean
    results.loc['%s'%name, 'Median time between trades'] = tbt1_median
    results.loc['%s'%name, 'Longest time between trades'] = tbt1_max

    results.loc['%s'%name, 'Mean time between tick changes'] = tbt2_mean
    results.loc['%s'%name, 'Median time between tick changes'] = tbt2_median
    results.loc['%s'%name, 'Longest time between tick changes'] = tbt2_max

    results.loc['%s'%name, 'Mean bid ask spread'] = spread_mean
    results.loc['%s'%name, 'Median bid ask spread'] = spread_median


    #new1.hist(column='Spread', bins= 12)
    #plt.show()


#Push to csv
results.to_csv('Results.csv')
    
print(results)


print('Done')




