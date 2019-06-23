#!/usr/bin/env python
# coding: utf-8

# In[285]:

## rewrite the Data Cleaning step into a function, for easy use on test data or combined data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats


# make a simple function that can take in a dictionary and convert the entire column values
# This function can be used over and over
def encod_catcoldf(df,dic:dict,col:str):
    """df: pandas dataframe; dic: dictionary that does the mapping for all possible values from desired column(1 column)"""
    """col: string format of the column name"""
    ext = df[col].values
    mapcol = [0]*len(df)
    for i,item in enumerate(ext):
        mapcol[i]=dic[item]

    df[col]=mapcol
    return df


def datacleanprep(df_fname,path=None):

    """""""""Only inputs are filename in string format, path in string format if file is not under current working folder. path variable is optional (default None)"""
    """Return processed pandas dataframe"""
    
    if path:readfname=path+df_fname
    else: readfname = df_fname

    data = pd.read_csv(readfname,index_col=0)

    """Working on Name column"""
    names = data.Name.values
    extract = {'Mr.':1,'Mrs.':2,'Miss.':3,'Ms.':4,'Master.':5,'Mrs':6,'Capt.':7,'Col.':8,'Rev.':9,'Dr.':10,'Don.':11,'Dona.':12,'Jonkheer.':13,'Lady.':14,'Major.':15,'Sir.':16,'Countess.':17,'Mlle.':18,'Mme.':19}
    """ a mapping dictionary for Names"""
    mapName =[0]*len(data)
    for i,item in enumerate(names):
        parse = str(item).split(' ')
        for parts in parse:
            if parts in extract.keys(): mapName[i]=extract[parts]

    """replace the 'Name' column """
    data['Name']=mapName

    """fill in the missing Age """

    """calculate mode of age based on 3 different cabin classes """
    sub_dt = data.loc[data.Pclass==1]
    a = np.array(sub_dt[sub_dt.Age.notnull()].Age)
    modc1 = stats.mode(a)[0][0]
    sub_dt = data.loc[data.Pclass==2]
    a = np.array(sub_dt[sub_dt.Age.notnull()].Age)
    modc2 = stats.mode(a)[0][0]
    sub_dt = data.loc[data.Pclass==3]
    a = np.array(sub_dt[sub_dt.Age.notnull()].Age)
    modc3 = stats.mode(a)[0][0]
    """create a mapping dictionary for average age in different cabin class"""
    mapAge = {1:modc1,2:modc2, 3:modc3}

    data['Age']=data['Age'].fillna(data['Pclass'].map(mapAge)) 
    """fill in mode number based on cabin class  to the training data"""

    """separate cabin text into two parts, cabin class and cabin number"""
    """Cabin class encode with assigned mapping, Cabin number use an average"""
    """separate the character and number in the Cabin column"""
    extCabin = data.Cabin.values

    extCabinTable = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'F G':8,'F E':9}
    mapCabin=[0]*len(data)

    for i,item in enumerate(data.Cabin.values):
        if item is not np.nan:
            parse = re.split('(\d+)',str(item))
            for parts in parse:
                if parts in extCabinTable.keys(): mapCabin[i]=extCabinTable[parts]

    data['CabinC']=mapCabin

    mapCabinN=[0]*len(data)
    for i,item in enumerate(data.Cabin.values):
        if item is not np.nan:
            parse = re.split('(\d+)',str(item))
            if len(parse)==1: continue
            # deal with the case that some rows missing Cabin number but with cabin char """
            tmp = [int(x) for x in parse[1:2]]
            mapCabinN[i]=np.mean(tmp)

    data['CabinN']=mapCabinN

    """ deal with missing values in Fare, if any (exist in testing data) """
    """ Get average ticket fare from 3 different cabin classes"""
    sub_df = data.loc[data.Fare.notnull()]
    avgf1 = np.mean(sub_df.loc[sub_df.Pclass==1].Fare.values)
    avgf2 = np.mean(sub_df.loc[sub_df.Pclass==2].Fare.values)
    avgf3 = np.mean(sub_df.loc[sub_df.Pclass==3].Fare.values)
    
    if sum(data.Fare.isnull()) != 0:
        if data.loc[data.Fare.isnull()].Pclass.values[0]==1: data['Fare']=data.Fare.fillna(value=avgf1)
        elif data.loc[data.Fare.isnull()].Pclass.values[0]==2: data['Fare']=data.Fare.fillna(value=avgf2)
        else: data['Fare']=data.Fare.fillna(value=avgf3)

    """Because the ticket Fare is highly related to the Cabin class(Pclass)"""    
    
    """ deal with missing values in Embarked """


    """Because the harbor which boarded most people is Southampton, I will assume these two records came from 'S' for simplicity (see data exploration)"""
    data['Embarked']=data.Embarked.fillna(value='S')

    """convert column 'Sex' and 'Embarked' """

    mapSex = {'female':0,'male':1}
    encod_catcoldf(data,mapSex,'Sex')

    mapEmb = {'C':0,'S':1,'Q':2}
    encod_catcoldf(data,mapEmb,'Embarked')


    """remove the column 'Ticket' and 'Cabin'(which is already separted into CabinC and CabinN)"""
    data = data.drop(columns=['Ticket','Cabin'], axis=1)

    """Done with the dataframe cleaning , return the result"""


    return data



