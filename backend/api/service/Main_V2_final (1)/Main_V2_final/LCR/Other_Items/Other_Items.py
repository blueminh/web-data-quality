"""
@Author: Gia Hieu
@Status: Completed
"""
import os
import pandas as pd
import numpy as np


path = os.path.dirname(os.path.realpath(__file__))


def lcr_Other_Items(path):
    df1 = pd.read_csv(os.path.join(path, 'input', 'Other Items.csv'))
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    
    #LCR
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
    df1['WEIGHTS'] = np.where(df1['WEIGHTS'].isnull()
                                                     ,0
                                                     ,df1['WEIGHTS'])
    df1['WEIGHTED AMOUNT FOR HQLA'] = df1['AMOUNT ALL MATURITY'] * df1['WEIGHTS']
    
    output_df['Amount all maturity'] = df1['AMOUNT ALL MATURITY']
    output_df['Amount under 6M'] = df1['AMOUNT UNDER 6M']
    output_df['Amount 6M to 1Y'] = df1['AMOUNT 6M TO 1Y']
    output_df['Amount above 1Y'] = df1['AMOUNT ABOVE 1Y']
    output_df['Weights'] = df1['WEIGHTS']
    output_df['Weighted amount for HQLA'] = df1['WEIGHTED AMOUNT FOR HQLA']
    final_output_df = df1.join(output_df)

    
    return final_output_df

final_output_df = lcr_Other_Items(path)
