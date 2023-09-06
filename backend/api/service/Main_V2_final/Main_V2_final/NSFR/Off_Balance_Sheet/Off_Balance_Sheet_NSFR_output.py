import pandas as pd
import numpy as np
import os
from ..Off_Balance_Sheet import Off_Balance_Sheet_output
from ...Input_Files import getFiles

def nsfr_offbalancesheet(input_date_str):
    df1 = getFiles.getFileByName("Off_Balance_Sheet" ,f'Off Balance Sheet_{input_date_str}.csv')
    df2 = Off_Balance_Sheet_output.lcr_offbalancesheet(input_date_str)
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    #output dataframe
   
    df1[' Unutilised Value '] = df1[' Unutilised Value '].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['RSF factor'] = pd.Series(np.full(df1['Off BS Account ID'].shape[0], 0.05))
    output_df['Unutilised Value'] = df1[' Unutilised Value ']
    
    output_df['RSF Amount'] = output_df['RSF factor'] * df1[' Unutilised Value ']
    final_output_df = df2.join(output_df)
    final_output_df = final_output_df.drop('Unutilised Value', axis=1)
    return final_output_df


