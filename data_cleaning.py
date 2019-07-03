#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 10:31:18 2018

@author: alex
"""

import json
from collections import Counter
import operator
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd

# load busdata
def loadbus():
    busdata = []
    file = open('business.json', 'r') #{}{}{}...
    for line in file.readlines():
        busdata.append(json.loads(line))
    return busdata

# load checkin data
def loadcheckin():
    checkindata = []
    file = open('checkin.json', 'r')
    for line in file.readlines():
        checkindata.append(json.loads(line))
    return checkindata
#print checkindata[0]#len(checkindata)

# load review data
def loadreview():
    reviewdata = []
    file = open('review.json', 'r')
    for line in file.readlines():
        reviewdata.append(json.loads(line))
    return reviewdata

# load user data
def loaduser():
    userdata = []
    file = open('user.json', 'r')
    for line in file.readlines():
        userdata.append(json.loads(line))
    return userdata

busdata = loadbus()
checkindata = loadcheckin()
#eviewdata = loadreview()
#userdata = loaduser()


# task1 find the 10 most popular business categories
# =============================================================================
# def catCounter():
#     busdata = loadbus()
#     cat = [d['categories'] for d in busdata]
#     cat = reduce(operator.add, cat)
#     counted = Counter(cat).most_common()[0:10]
#     for c in counted:
#         print c
# =============================================================================

# task2 find the 10 most popular business objects
def checkinCounter():
    
    collection = []
    
    # count weekly checkin for each business object
    for bo in checkindata:
        count = 0
        for day in bo['time']:
            for hour in bo['time'][day]:
                count += bo['time'][day][hour]
        collection.append((count, bo['business_id']))
    
# =============================================================================
    bolist = [y for (x,y) in sorted(collection, key=lambda x: x[0], reverse=True)[0:10]]
    
    # find bo.json for each bo
    boinfo = [b for b in busdata if b['business_id'] in bolist]
            
    # make a dataframe to show info
    df = json_normalize(boinfo)[['name', 'city', 'state']]
    df['category'] = [b['categories'][0] for b in boinfo]
    df['checkin'] = [x for (x,y) in sorted(collection, key=lambda x: x[0], reverse=True)[0:10]]
    
    print df
    

# collect business ids based on categories
def getid(cat): # a string with first letter cap
    
    idlist = []
    for d in busdata:
        if cat in d['categories']:
            idlist.append(d['business_id'])
    return idlist

  
# merge data under a specific category into a dataframe: 
# columns: busid, text, funny, useful, cool, stars, userid, fans, user_useful, user_cool, user_funny
# output a .csv file
def mergedata():
    
    # busid, cool, funny, stars, text, useful, user_id from review.json
    dfreview = json_normalize(reviewdata).drop(['date', 'review_id'] ,1)
    # user_id, fans, user_funny, user_useful, user_cool
    dfuser = json_normalize(userdata)[['user_id', 'fans', 'cool', 'funny', 'useful']]
    dfuser = dfuser.rename(columns={'cool':'user_cool', 'funny': 'user_funny', 'useful': 'user_useful'})
    
    # generate a list of target bus ids
    ids = getid('Restaurants')
    # customize the dataframe with only the desired bus category
    dfcat = dfreview[dfreview['business_id'].isin(ids)]
    
    # merge dfreview and dfuser on user_id
    dfmerge = pd.merge(dfreview, dfuser, on='user_id', how='inner')
    dfcatmerge = pd.merge(dfcat, dfuser, on='user_id', how='inner').head(10000)
    
    # write data to csv
    #dfmerge.to_csv('dfComplete.csv', encoding='utf-8') # complete data 
    #dfcatmerge.to_csv('dfRestaurantstest.csv', encoding='utf-8') # data under the Restaurants category
    
    #return dfmerge.to_csv('dfRestaurants.csv', encoding='utf-8')
    #return dfcatmerge.to_csv('dfRestaurants.csv', encoding='utf-8')

#mergedata()

### get IL specific data ###############################################################
# convert busdata to dataframe
df = json_normalize(busdata)
# load dfComplete.csc file
types_dict = {'funny': 'int64',
              'Unnamed: 0': 'O',
              'user_cool': 'float64',
              'user_id': 'O',
              'text': 'O',
              'business_id': 'O',
              'user_funny': 'float64',
              'user_useful': 'float64',
              'fans': 'float64',
              'stars': 'int64',
              'useful': 'float64',
              'cool': 'O'}
data = pd.read_csv('dfComplete.csv', dtype=types_dict, low_memory=True)
# extract business_id data and combine with state data
busid = pd.DataFrame(data=data['business_id'])
idstate = pd.merge(busid, df[['business_id', 'state']], on='business_id', how='inner')
# extract IL-specific data from the dfComplete file
ILid = idstate[idstate['state'] == 'IL']['business_id'].tolist()
ILdf = data[data['business_id'].isin(ILid)].drop(['business_id', 'user_id'], axis=1)
#ILdf.to_csv('IL.csv', encoding='utf-8', index=False)


