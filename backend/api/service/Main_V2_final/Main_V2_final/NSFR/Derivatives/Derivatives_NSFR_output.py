import pandas as pd
import numpy as np
import os
from ..Derivatives import Derivatives_output
from ...Input_Files import getFiles

def nsfr_derivatives(input_date_str):

    df1 =  getFiles.getFileByName("Derivatives", f'Derivatives_{input_date_str}.csv')
    df2 =  Derivatives_output.lcr_derivatives(input_date_str)

    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()
    df1['MTM'] = df1['MTM'].str.replace(',', '')
    df1['MTM'] = df1['MTM'].apply(lambda x: float(x.replace('(', '-').replace(')', '')) if isinstance(x, str) else x)

    total_assets = df1[df1['MTM'] > 0]['MTM'].sum()
    output_df.loc[0, 'Total Derivatives Assets'] = total_assets
    total_derivatives_liabilities = abs(df1[df1['MTM'] < 0]['MTM'].sum())
    output_df.loc[0, 'Total Derivatives Liabiilities'] = total_derivatives_liabilities



    output_df['Net Derivative Amount'] = output_df.loc[0, 'Total Derivatives Assets'] - output_df.loc[0, 'Total Derivatives Liabiilities']

    output_df['ASF Amount'] = np.where(output_df['Net Derivative Amount'] < 0, 0, 0)

    output_df['RSF Amount'] = np.where(output_df['Net Derivative Amount'] > 0, 
                                    np.maximum(1*output_df.loc[0, 'Total Derivatives Assets'] - 0.05*abs(output_df.loc[0, 'Total Derivatives Liabiilities']), 0), 
                                    0)


    final_output_df = df2.join(output_df)
    return final_output_df

