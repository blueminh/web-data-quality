"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date
from ...Input_Files import getFiles

# Đường dẫn đến file
path = os.path.dirname(os.path.realpath(__file__))

def lcr_sanctionedloans(path):
    # Reporting date
    reporting_date = date(2022, 9, 30)

    df1 = getFiles.getFileByName("Sanctioned_Loans", 'Sanctioned Loans.csv')

    #output dataframe
    output_df = pd.DataFrame()
    output_df['Reporting Date'] = pd.Series(np.full(df1['Due Disbursement Date'].shape[0], reporting_date), dtype='datetime64[ns]')

    # Chuyển đổi định dạng ngày tháng trong df1
    valid_dates_df1 = pd.to_datetime(df1['Due Disbursement Date'], errors='coerce')

    # Lọc bỏ các giá trị không hợp lệ trong df1
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]

    output_df['Days to Maturity'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days < 0,
        '30 or Less',
        np.where((valid_dates_df1 - output_df['Reporting Date']).dt.days <= 30, '30 or Less', 'More Than 30 Days')
    )
    df1[' Due Disbursement Amount '] = df1[' Due Disbursement Amount '].str.replace(',', '').astype(float)
    output_df['Runoff Factor'] = 1
    output_df['Cash Outflow'] = np.where(
        output_df['Days to Maturity'] == '30 or Less',
        df1[' Due Disbursement Amount '] * output_df['Runoff Factor'],
        0
    )

    output_df['Cash Outflow'] = output_df['Cash Outflow'].apply(lambda x: '{:,}'.format(x))


    final_output_df = df1.join(output_df)
    final_output_df = final_output_df.head(12)
    return final_output_df


final_output_df = lcr_sanctionedloans(path)



