#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Program: Final_Project_harsh_03
Author: Harshit Yadav
Purpose: Program to generate graphical representation of selected  data
Revisions: Step 1: Print program name
           read data from fike
           get list of locations
           change the date format
           convert data into  individual record

           Step2: Forming lists commodity,date,location
           Printing data and asking user input
           according to the data

           Step3: Data consolidation for selected dates
           Computing average price of selected  commodities
           Plotting graph

'''

import csv
from datetime import datetime as dt
import plotly.offline as po
import plotly.graph_objs as pg
def average(a):
#Function to return average price of list.

    return sum(a)/len(a)
#Step 1: Print program name
#        read data from fike
#        get list of locations
#        change the date format
#        conver data into  individual record
print("="*26)
print('Analysis of Comodity Data')
print("="*26)
#program heading
with open('produce_csv.csv','r') as csvfile:
#read data of file
    reader=csv.reader(csvfile)
    data=[row for row in reader]
locations=data.pop(0)[2:]
#pop and slice for location
for row in data:
#chang format of data 
    for i,item in enumerate(row):
        if '$' in item:
            row[i]=float(item.replace('$',""))
#replace character '$' with space
for i,item in enumerate(data):
    data[i][1]=dt.strptime(item[1],"%m/%d/%Y")
#format the date
records=[]
for row in data:
#convert the data in the indicidual record
    for loc,price in zip(locations,row[2:]):
        records.append(row[:2]+[loc,price])
        
#Step2: Form list of location , date and community
#       Print the data and ask  user input
#       according to the data
commodity=sorted(list(set([a[0] for a in records])))
#list of commodities
print('\nSELECT PRODUCT BY NUMBER ...')
[print(f"<{i}> {j}") for i,j in enumerate(commodity)]
#enumerate  the list for print the index and the commodities
com_number=[int(x) for x in input("Enter product numbers seperated by space: ").split()]
#ask user for input
com_select=[commodity[item] for item in com_number]
#list of user selected commodities
print("Selected products are: ",end="")
[print(commodity[item]+' ',end='') for item in com_number]
#print the commodities by user
date=sorted(list(set([a[1] for a in records])))
#list for all the dates
print('\n\nSELECT DATE RANGE BY NUMBER ...')
[print(f"<{i}> {dt.strftime(j,'%Y-%m-%d')}") for i,j in enumerate(date)]
#enumerate  the list for printing index and the dates
print('Earliest available date is: ',dt.strftime(date[0],'%Y-%m-%d'))
#printing earliest date
print('Latest available date is: ',dt.strftime(date[-1],'%Y-%m-%d'))
#printing latest date
all_date=[int(x) for x in input("Enter start/end date numbers seperated by a space: ").split()]
#asking user for input
dates=[dt.strftime(date[item],'%Y-%m-%d')for item in all_date]
#list of selected dates by user
print("Dates from: ",end="")
[print(dates[0],'to',dates[1])]
#print dates
start_date=dt.strptime(dates[0],'%Y-%m-%d')
#start date by user
end_date=dt.strptime(dates[1],'%Y-%m-%d')
#end date by user
location=sorted(list(set([a[2] for a in records])))
#list of all locations 
print('\nSELECT LOCATIONS BY NUMBER ...')
[print(f"<{i}> {j}") for i,j in enumerate(location)]
#enumerate the list for printing index and locations
loc_number=[int(x) for x in input("Enter location numbers separated by spaces: ").split()]
#asking user for input
loc_select=[location[item] for item in loc_number]
#list of selected locations
print("Selected locations are: ",end="")
[print(location[item]+' ',end="") for item in loc_number]
#printing locations
all_select=list(filter(lambda x:x[0] in com_select and (start_date<=x[1]<=end_date) and x[2] in loc_select,records))
#selecting data specific to the user selection
print(f'\n{len(all_select)} records have been selected.')

#Step3: Data consolidation for selected
#       dates
#       Calculate the average
#       commodities
#       Plotting graph
doc={}
for i in loc_select:
#consolidate data for selected dates
    doc[i]={}
    for j in com_select:
        doc[i].update({j:[]})
        doc[i][j]=[x[3] for x in all_select if x[2]==i and x[0]==j]
plot={}
for k in doc:
#calculate the  average
    plot.update({k:{}})
    for l in doc[k]:
        plot[k].update({l:average(doc[k][l])})
#call the function
trace=[]
for loc in loc_select:
#plot the graph
    all_price=[plot[loc][com] for com in com_select]
    trace.append(pg.Bar(x=com_select,y=all_price,name=loc))
layout=pg.Layout(barmode='group')
#bar graph
fig=pg.Figure(data=trace,layout=layout)
fig.update_layout(
    title=f'Product prices from {dates[0]} through {dates[1]}',
    xaxis_title="Product",
    yaxis_title="Average Price"
#printing axis
    )
fig.update_layout(yaxis_tickformat='$.2f')
#formating
po.plot(fig,filename='grouped-bar.html')
#naming
fig.show()


# In[ ]:




