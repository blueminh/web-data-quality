import pandas as pd
import numpy as np
import warnings
import os
from ..Deposits_with_Other_Bank import Deposits_with_other_banks_output
warnings.filterwarnings('ignore')
from ...Input_Files import getFiles

def NSFR_Deposits_with_Other_Banks(input_date_str):
    df1 = getFiles.getFileByName("Deposits_with_other_banks", f'Deposits with Other Banks_{input_date_str}.csv')
    df2 = Deposits_with_other_banks_output.lcr_deposits(input_date_str)
    output_df = pd.DataFrame()
    #df1.fillna(0, inplace=True)
    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')
    
    # Chắc chắn df1 và df2 có cùng số lượng dòng trước khi trừ nhau.    
    day_diff = (df1['Maturity Date'] - df2['Reporting Date']).dt.days
    
    conditions = [
        df1['Maturity Date'].isna(),
        day_diff > 360,
        (day_diff > 180) & (day_diff <= 360),
        day_diff <= 180
    ]
    
    choices = [
        "No Maturity",
        "More than 1 year",
        "6 months to 1 year",
        "Less than 6 months"
    ]
    
    # Giả sử bạn muốn gán giá trị cho cột 'Maturity Bucket' trong df1
    output_df['Maturity Bucket'] = np.select(conditions, choices, default="Unknown")


    conditions = [
        (df1['Operational'] == 'yes'),
        (output_df['Maturity Bucket'] == 'Less than 6 months'),
        (output_df['Maturity Bucket'] == '6 months to 1 year'),
        (output_df['Maturity Bucket'] == 'More than 1 year'),
        (output_df['Maturity Bucket'] == 'No Maturity')]

    choices = [0.5, 0.15, 0.5, 1, 1]

    output_df['RSF Factor'] = np.select(conditions, choices, default=np.nan)
    df1['Deposit balance'] = df1['Deposit balance'].str.replace(',', '').astype(float)

    output_df['RSF Amount'] = df1['Deposit balance'] * output_df['RSF Factor']

    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    day_diff = (df1['Maturity Date'] - df2['Reporting Date']).dt.days
    output_df['Remaining Maturity for Accrued Interest'] = np.where(df1['Next Interest Payment Due Date'].isnull(), 'No Accrued Interest', 
                                                                np.where(day_diff > 360, "More than 1 year", 
                                                                         np.where(day_diff > 180, "6 months to 1 year", "Less than 6 months")))

    output_df['RSF Factor for Accrued Interest'] = 1
    output_df['RSF Amount for Accrued Interest'] = output_df['RSF Factor for Accrued Interest'] * df1['Accrued Interest'].fillna(0)
    output_df['Total RSF Amount'] = output_df['RSF Amount for Accrued Interest'] + output_df['RSF Amount']
    final_output_df = df2.join(output_df)

    return final_output_df


