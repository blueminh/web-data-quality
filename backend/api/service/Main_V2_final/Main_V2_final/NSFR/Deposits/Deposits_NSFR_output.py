import os
import numpy as np
import pandas as pd

from .Deposit import Deposits_output


path = os.path.dirname(os.path.realpath(__file__))

def nsfr_deposits(path):
    df1 = pd.read_csv(os.path.join(path, 'Deposit', 'input', 'Deposit.csv'))
    df2 = Deposits_output.Deposits_LCR(os.path.join(path, 'Deposit'))
    df3 = pd.read_csv(os.path.join(path, 'Deposit', 'input', 'Less Stable Deposit Mapping.csv'))
    df4 = pd.read_csv(os.path.join(path,  'Deposit','input', 'Stable Deposit Mapping.csv'))

    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')

    day_diff = (df1['Maturity Date'] - df2['Reporting Date']).dt.days

    conditions = [
        ((df2['Maturity Date'] == 0) & (df2['Product type'] == 'Demand Deposit')),
        (day_diff >= 360),
        (day_diff >= 180)
    ]


    choices = [
        'No Maturity',
        'More than 1 year',
        '6 months to 1 year'
        ]

    output_df['Days to Maturity'] = np.select(conditions, choices, default='Less than 6 months')

    df2['Lookup Key'] = df2['Product type'] + df2['Retail/Wholesale'] + output_df['Days to Maturity'] + df1['Significant Penalty Flag']
    df4['Lookup Key'] = df4['Concat']
    merged_df = pd.merge(df2, df4[['Lookup Key', 'ASF Factor']], on='Lookup Key', how='left')
    output_df['Stable ASF Factor'] = merged_df['ASF Factor']

    df2['Lookup Key'] = df2['Product type'] + output_df['Days to Maturity'] + df2['Retail/Wholesale'] + df1['Significant Penalty Flag']
    df3['Lookup Key'] = df3['Concat']
    merged_df = pd.merge(df2, df3[['Lookup Key', 'ASF Factor']], on='Lookup Key', how='left')
    output_df['Unstable ASF Factor'] = merged_df['ASF Factor']

    df1['Deposit balance'] = df1['Deposit balance'].str.replace(',', '').replace(' -   ', '0').astype(float)
    conditional_sum = df1[df2['Volatile Flag'] == "No"].groupby('Customer ID')['Deposit balance'].transform('sum')
    
    
    min_val = np.minimum(df1['Deposit balance'] / conditional_sum * df2['Insured Amount/Customer'], df1['Deposit balance'])
    output_df['Principal Stable Amount'] = np.where(df2['Volatile Flag'] == "No", min_val, 0)
    output_df['Principal Stable Amount'] = output_df['Principal Stable Amount'].fillna(0.0)


    output_df['Principal Unstable Amount'] = df1['Deposit balance'] - output_df['Principal Stable Amount']
    output_df['Stable ASF Factor'] = output_df['Stable ASF Factor'].str.rstrip('%').astype('float') / 100.0
    output_df['Principal Stable Amount'] = output_df['Principal Stable Amount'].astype(float)
    output_df['Weighted Stable Amount'] = output_df['Stable ASF Factor'] * output_df['Principal Stable Amount']
    output_df['Unstable ASF Factor'] = output_df['Unstable ASF Factor'].str.rstrip('%').astype('float') / 100.0 
    output_df['Principal Unstable Amount'] = output_df['Principal Unstable Amount'].astype(float)
    output_df['Weighted Unstable Amount'] =  output_df['Unstable ASF Factor'] * output_df['Principal Unstable Amount']

    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df1['Start Date'] = pd.to_datetime(df1['Start Date'], errors='coerce')

    day_diff = (df1['Maturity Date'] - df1['Start Date']).dt.days

    output_df['Remaining Maturity for Accrued Interest'] = np.where(day_diff >= 360, "More than 1 year", 
                                             np.where(day_diff >= 180, "6 months to 1 year", "Less than 6 months"))

    conditions = [
        (output_df['Remaining Maturity for Accrued Interest'] == 'Less than 6 months'),
        (output_df['Remaining Maturity for Accrued Interest'] == '6 months to 1 year'),
        (output_df['Remaining Maturity for Accrued Interest'] == 'More than 1 year')
        ]
    values = [0.0, 0.5, 1.0]
    output_df['ASF factor for Accrued Interest'] = np.select(conditions, values)

    output_df['ASF factor for Accrued Interest'] = output_df['ASF factor for Accrued Interest'].astype(float)
    output_df['ASF Amount for Accrued Interest'] = df1[' Accrued Interest '] * output_df['ASF factor for Accrued Interest']

    output_df['Total Weighted Deposit Balance Amount'] = output_df['Weighted Stable Amount'] + output_df['Weighted Unstable Amount']

    final_output_df = df2.join(output_df)
    final_output_df = final_output_df.drop('Lookup Key', axis=1)
    return final_output_df

#output file
