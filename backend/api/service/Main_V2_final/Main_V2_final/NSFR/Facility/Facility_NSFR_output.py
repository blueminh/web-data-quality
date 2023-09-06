"""
@Author: Minh Anh
@Status: Completed
"""
import pandas as pd
import numpy as np
import os
from ...Input_Files import getFiles

def nsfr_facility(input_date_str):
    df1 =  getFiles.getFileByName("Facility", f'Facility_{input_date_str}.csv')

    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()
    
    output_df['RSF Factor Undrawn Amt'] = pd.Series(np.full(df1['Facility ID'].shape[0], 0.05))
    df1[' Undrawn Credit Line '] = df1[' Undrawn Credit Line '].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['RSF Amount Undrawn'] = output_df['RSF Factor Undrawn Amt'] * df1[' Undrawn Credit Line ']
    final_output_df = df1.join(output_df)

    return final_output_df

