"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date

# Đường dẫn đến file
path = os.path.dirname(os.path.realpath(__file__))
def lcr_deposits(path):
    # Reporting date
    reporting_date = date(2022, 9, 30)

    df1 = pd.read_csv(os.path.join(path, 'input', 'Deposits with Other Banks.csv'))
    df1.fillna(0, inplace=True)
    output_df = pd.DataFrame()
    #reporting date
    output_df['Reporting Date'] = pd.Series(np.full(df1['Account ID with FI'].shape[0], reporting_date), dtype='datetime64[ns]')


    # Convert date columns to datetime format
    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df1['Next Interest Payment Due Date'] = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    #Days to Maturity
    valid_dates_df1 = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    output_df['Days to Maturity'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less'
    )
    output_df.loc[df1['Maturity Date'] == 0,'Days to Maturity'] = '30 or Less'
    
    #Days till next interet payment
    valid_dates_df1 = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    output_df['Days to Next Interest Payment'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less'
    )
    output_df.loc[df1['Next Interest Payment Due Date'] == 0,'Days to Next Interest Payment'] = '30 or Less'
    # Calculate inflow rate
    output_df['Inflow Rate'] = np.where((df1['Operational'] == 0) | (df1['Operational'] == "No"), 1, 0)
    df1['Deposit balance'] = df1['Deposit balance'].str.replace(',', '').astype(float)
    df1['Interest Receivable']=df1['Interest Receivable'].str.replace(',', '').astype(float)

    inflow_from_maturity = np.where(output_df['Days to Maturity'] == "30 or Less", df1['Deposit balance'], 0)
    inflow_from_interest = np.where(output_df['Days to Next Interest Payment'] == "30 or Less", df1['Interest Receivable'], 0)
    
    # Kiểm tra nếu 'Interest Receivable' bị trống
    is_interest_receivable_empty = df1['Interest Receivable'].isna()
    
    # Tính toán cho Inflow dựa trên điều kiện
    output_df['Inflow'] = np.where(is_interest_receivable_empty,
                                   inflow_from_maturity * output_df['Inflow Rate'],
                                   (inflow_from_maturity + inflow_from_interest) * output_df['Inflow Rate'])



    
    final_output_df = df1.join(output_df)

    return final_output_df
