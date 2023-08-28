"""
@Author: Gia Hieu
@Status: Completed
"""
import pandas as pd
import numpy as np
import os

path = os.path.dirname(os.path.realpath(__file__))


def nsfr_New_Other_Items(path):
    df1 = pd.read_csv(os.path.join(path, 'input', 'Other_Items.csv'))
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    #nsfr
    df1['AMOUNT ALL MATURITY'] = df1['AMOUNT ALL MATURITY'].str.replace(',', '').replace(' -   ', '0').astype(float)

    df1['AMOUNT UNDER 6M'] = df1['AMOUNT UNDER 6M'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['AMOUNT 6M TO 1Y'] = df1['AMOUNT 6M TO 1Y'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['AMOUNT ABOVE 1Y'] = df1['AMOUNT ABOVE 1Y'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['WEIGHTS'] = df1['WEIGHTS'].str.rstrip('%').astype('float') / 100.0
    
    df1['AMOUNT ALL MATURITY'] = np.where(df1['AMOUNT ALL MATURITY'].isnull()
                                                     ,0
                                                     ,df1['AMOUNT ALL MATURITY'])
    df1['AMOUNT UNDER 6M'] = np.where(df1['AMOUNT UNDER 6M'].isnull()
                                                     ,0
                                                     ,df1['AMOUNT UNDER 6M'])
    df1['AMOUNT 6M TO 1Y'] = np.where(df1['AMOUNT 6M TO 1Y'].isnull()
                                                     ,0
                                                     ,df1['AMOUNT 6M TO 1Y'])
    df1['AMOUNT ABOVE 1Y'] = np.where(df1['AMOUNT ABOVE 1Y'].isnull()
                                                     ,0
                                                     ,df1['AMOUNT ABOVE 1Y'])
    df1['RSF FACTOR ALL MATURITY'] = df1['RSF FACTOR ALL MATURITY'].str.rstrip('%').astype('float') / 100.0
    df1['ASF FACTOR UNDER 6M'] = df1['ASF FACTOR UNDER 6M'].str.rstrip('%').astype('float') / 100.0
    df1['ASF FACTOR 6M TO 1Y'] = df1['ASF FACTOR 6M TO 1Y'].str.rstrip('%').astype('float') / 100.0
    df1['ASF FACTOR ABOVE 1Y'] = df1['ASF FACTOR ABOVE 1Y'].str.rstrip('%').astype('float') / 100.0
 
    df1['RSF FACTOR ALL MATURITY'] = np.where(df1['RSF FACTOR ALL MATURITY'].isnull()
                                                  ,0
                                                  ,df1['RSF FACTOR ALL MATURITY'])
    df1['ASF FACTOR UNDER 6M'] = np.where(df1['ASF FACTOR UNDER 6M'].isnull()
                                                  ,0
                                                  ,df1['ASF FACTOR UNDER 6M'])
    df1['ASF FACTOR 6M TO 1Y'] = np.where(df1['ASF FACTOR 6M TO 1Y'].isnull()
                                                  ,0
                                                  ,df1['ASF FACTOR 6M TO 1Y'])
    df1['ASF FACTOR ABOVE 1Y'] = np.where(df1['ASF FACTOR ABOVE 1Y'].isnull()
                                                  ,0
                                                  ,df1['ASF FACTOR ABOVE 1Y'])
    df1['WEIGHTED RSF AMOUNT'] = df1['RSF FACTOR ALL MATURITY'] * df1['AMOUNT ALL MATURITY']
    
    conditions = [
        (df1['TYPE'] == 'LIABILITIES'),
        (df1['TYPE'] == 'EQUITIES')
    ]
    
    choices = [
        df1['ASF FACTOR UNDER 6M'] * df1['AMOUNT UNDER 6M'] + df1['ASF FACTOR 6M TO 1Y'] * df1['AMOUNT 6M TO 1Y'] + df1['ASF FACTOR ABOVE 1Y'] * df1['AMOUNT ABOVE 1Y'],
        df1['ASF FACTOR ABOVE 1Y'] * df1['AMOUNT ABOVE 1Y']
    ]
    
    df1['WEIGHTED ASF AMOUNT'] = np.select(conditions, choices, default=0)

   
    
    output_df['Amount all Maturity'] = df1['AMOUNT ALL MATURITY']
    output_df['Amount under 6M'] = df1['AMOUNT UNDER 6M']
    output_df['Amount 6M To 1Y'] = df1['AMOUNT 6M TO 1Y']
    output_df['Amount Above 1Y'] = df1['AMOUNT ABOVE 1Y']
    output_df['RSF Factor all Maturity'] = df1['RSF FACTOR ALL MATURITY']
    output_df['ASF Factor under 6M'] = df1['ASF FACTOR UNDER 6M']
    output_df['ASF Factor 6M TO 1Y'] = df1['ASF FACTOR 6M TO 1Y']
    output_df['ASF Factor Above 1Y'] = df1['ASF FACTOR ABOVE 1Y']
    output_df['Weighted RSF Amount'] = df1['WEIGHTED RSF AMOUNT']
    output_df['Weighted ASF Amount'] = df1['WEIGHTED ASF AMOUNT']

    final_output_df = df1.join(output_df)

    return final_output_df


final_output_df = nsfr_New_Other_Items(path)
