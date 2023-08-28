"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Đường dẫn đến file
path = os.path.dirname(os.path.realpath(__file__))

def lcr_borrowing(path, input_date_str):
    input_date = datetime.strptime(input_date_str, "%d-%m-%Y")
    borrowings_filename = f"Borrowings_{input_date_str}.csv"
    df1 = pd.read_csv(os.path.join(path, 'input', borrowings_filename))
    df2 = pd.read_csv(os.path.join(path, 'input', 'Counterparty Mapping.csv'))
    df3 = pd.read_csv(os.path.join(path, 'input', 'Counterparty Unsecured Funding Mapping.csv'))
# Tạo DataFrame mới để chứa kết quả tính toán
    # Tạo DataFrame mới để chứa kết quả tính toán
    output_df = pd.DataFrame()
    reporting_date = input_date.date()
    df1.fillna(0, inplace=True)

    # Tạo cột "Reporting Date" với số lượng dòng tương ứng với cột "Instrument Id" của df1

    output_df['Reporting Date'] = pd.Series(np.full(df1['Instrument Id'].shape[0], reporting_date), dtype='datetime64[ns]')
    # Chuyển đổi định dạng ngày tháng trong df1
    valid_dates_df1 = pd.to_datetime(df1['Next principal payment due date'], errors='coerce')

    # Lọc bỏ các giá trị không hợp lệ trong df1
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]
    
    output_df['Days To Next Principal Payment'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days < 0,
        '30 or Less',
        np.where((valid_dates_df1 - output_df['Reporting Date']).dt.days <= 30, 
        '30 or Less', 
        'More Than 30 Days')
    )
    output_df.loc[df1['Next principal payment due date'] == 0, 'Days To Next Principal Payment'] = '30 or Less'



    # Merge df1 và df2 dựa trên cột 'Customer Type' và 'Counterparty Type'
    merged_df = df1.merge(df2[['Counterparty Type', 'Counterparty Category']], 
                          left_on='Customer Type', 
                          right_on='Counterparty Type', 
                          how='left')

    # Tạo cột 'Counterparty Category' trong dataframe output_df từ cột 'Counterparty Category' của merged_df
    output_df['Counterparty Category'] = merged_df['Counterparty Category']

    # Merge output_df và df3 dựa trên cột 'Counterparty Category'
    merged_df = output_df.merge(df3[['Counterparty Category', 'Run Off Factor']], 
                                left_on='Counterparty Category', 
                                right_on='Counterparty Category', 
                                how='left')

    # Merge output_df và df3 dựa trên cột 'Counterparty Category'
    merged_df = output_df.merge(df3[['Counterparty Category', 'Run Off Factor']], 
                                left_on='Counterparty Category', 
                                right_on='Counterparty Category', 
                                how='left')

    # Kiểm tra và gán giá trị "30 or Less" cho những ô trống của cột 'Days To Next Principal Payment'
    output_df['Days To Next Principal Payment'] = np.where(
        df1['Next principal payment due date'] == 0,
        '30 or Less',
        output_df['Days To Next Principal Payment']
    )

    # Tạo cột 'RunOff Factor' trong dataframe output_df từ cột 'Run Off Factor' của merged_df
    output_df['RunOff Factor'] = merged_df['Run Off Factor'] 
    output_df['RunOff Factor'] = output_df['RunOff Factor'].str.rstrip('%').astype(float) 
    df1['Next principal payment Amount'] = df1['Next principal payment Amount'].str.replace(',', '').astype(float)
    output_df['Weighted Principal Cash Outflow'] = np.where(
        output_df['Days To Next Principal Payment'] == '30 or Less',
        df1['Next principal payment Amount'] * output_df['RunOff Factor'] / 100,
        0
    )

    # Chuyển đổi định dạng ngày tháng trong df1
    valid_dates_df1 = pd.to_datetime(df1['Next interest payment due date'], errors='coerce')
    output_df['Difference'] = valid_dates_df1 - output_df['Reporting Date']
    output_df['Days To Coupon'] = np.where(
        output_df['Difference'].dt.days < 0,
        '30 or Less',
        np.where(output_df['Difference'].dt.days <= 30, '30 or Less', 'More Than 30 Days')
    )
    output_df.drop('Difference', axis=1, inplace=True)

    # Kiểm tra và gán giá trị "30 or Less" cho những ô trống của cột 'Days To Next Principal Payment'
    output_df['Days To Coupon'] = np.where(
        df1['Next interest payment due date'] == 0,
        '30 or Less',
        output_df['Days To Coupon']
    )
    df1['Next Interest Payment Amount'] = df1['Next Interest Payment Amount'].replace('', '0')
    df1['Next Interest Payment Amount'] = df1['Next Interest Payment Amount'].astype(float)

    output_df['Weighted Coupon Cash Outflow'] = np.where(
        output_df['Days To Coupon'] == '30 or Less',
        output_df['RunOff Factor'] / 100 * df1['Next Interest Payment Amount'],
        0
    )

    output_df['Total Weighted Cash Outflow'] = output_df['Weighted Coupon Cash Outflow'] + output_df['Weighted Principal Cash Outflow']
    output_df['RunOff Factor']=output_df['RunOff Factor'] / 100

# Concatenate df1 and output_df along the column axis.
    final_output_df = df1.join(output_df)

    return final_output_df

final_output_df = lcr_borrowing(path, "28-08-2023")