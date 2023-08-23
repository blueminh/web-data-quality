"""
@Author: Minh Anh
@Status: Completed
"""
import pandas as pd
import numpy as np
import os

path = os.path.dirname(os.path.realpath(__file__))

def nsfr_facility(path):
    df1 =  pd.read_csv(os.path.join(path, 'input', 'Facility.csv'))

    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()
    
    output_df['RSF Factor Undrawn Amt'] = pd.Series(np.full(df1['Facility ID'].shape[0], 0.05))
    df1[' Undrawn Credit Line '] = df1[' Undrawn Credit Line '].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['RSF Amount Undrawn'] = output_df['RSF Factor Undrawn Amt'] * df1[' Undrawn Credit Line ']
    final_output_df = df1.join(output_df)

    return final_output_df

#output file
final_output_df = nsfr_facility(path)
