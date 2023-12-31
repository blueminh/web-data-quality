import numpy as np
import pandas as pd
import os
from ..Issued_Securities import Issued_Securities
from ...Input_Files import getFiles

def Issued_Securities_NSFR(input_date_str):
    input_folder_path = "Issued_Securities"
    df1 = getFiles.getFileByName(input_folder_path, f'Issued_Securities_{input_date_str}.csv')
    df2 = Issued_Securities.lcr_Issued_Securities(input_date_str)
    df3 = getFiles.getMappingFileByName('ISSUED_SECURITIES_AND_BORROWINGS_MAPPING.csv')

    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)

    df1['Instrument Maturity Date'] = pd.to_datetime(df1['Instrument Maturity Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')

    day_diff = (df1['Instrument Maturity Date'] - df2['Reporting Date']).dt.days

    output_df['Remaining Maturity'] = np.where(day_diff >= 360, "More than 1 year",
                                          np.where(day_diff < 180, "Less than 6 months", 
                                                   "6 months to 1 year"))

    df2['Concat'] = df2['Counterparty Category'].astype(str) + output_df['Remaining Maturity']
    merged_df = pd.merge(df2, df3[['Concat', 'ASF Factor']], on='Concat', how='left')
    output_df['ASF Factor'] = merged_df['ASF Factor']
    output_df['ASF Factor'] =output_df['ASF Factor'].str.replace('%', '').astype(float) / 100.0
    df1['Book Value'] =df1['Book Value'].str.replace(',', '').astype(float)
    conditions = [
        (df1['Included in Capital Tier 2'] == ' No '),
        (df1['Included in Capital Tier 2'] == ' Yes ') & (output_df['Remaining Maturity'] != 'More than 1 year')
    ]
    choices = [
        output_df['ASF Factor'] * df1['Book Value'],
        output_df['ASF Factor'] * df1['Book Value']
    ]
    
    output_df['ASF Amount'] = np.select(conditions, choices, default=0)

    df1['Next Interest Payment Due Date'] = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')

    day_diff = (df1['Next Interest Payment Due Date'] - df2['Reporting Date']).dt.days

    output_df['Remaining Maturity for Accrued Interest'] = np.where(day_diff >= 360, "More than 1 year",
                                                                np.where(day_diff < 180, "Less than 6 months", 
                                                                         "6 months to 1 year"))

    conditions = [(output_df['Remaining Maturity for Accrued Interest'] == "Less than 6 months"),
        (output_df['Remaining Maturity for Accrued Interest'] == "6 months to 1 year"),
        (output_df['Remaining Maturity for Accrued Interest'] == "More than 1 year")
        ]

    choices = [0, 0.5, 1]

    output_df['ASF factor for Accrued Interest'] = np.select(conditions, choices, default=np.nan)
    
    df1['Accrued Interest'] = df1['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['ASF Amount for Accrued Interest'] = output_df['ASF factor for Accrued Interest'] * df1['Accrued Interest']

    output_df['Total ASF Amount'] = output_df['ASF Amount for Accrued Interest'] + output_df['ASF Amount']
    final_output_df = df2.join(output_df)
    final_output_df =final_output_df.drop('Concat', axis=1)
    final_output_df['Book Value'] = final_output_df['Book Value'].str.replace(',', '').astype(float)
    final_output_df['Accrued Interest'] = final_output_df['Accrued Interest'].str.replace(',', '').astype(float)
    return final_output_df
