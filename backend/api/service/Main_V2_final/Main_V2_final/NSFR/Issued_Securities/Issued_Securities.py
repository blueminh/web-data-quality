"""
@Author: Minh Anh & Gia Hieu
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date

def lcr_Issued_Securities():
    path = os.path.dirname(os.path.realpath(__file__))
    df1 = pd.read_csv(os.path.join(path, 'input', 'Issued Securities.csv'))
    df2 = pd.read_csv(os.path.join(path, 'input', 'CounterParty Mapping.csv'))
    df4 = pd.read_csv(os.path.join(path, 'input', 'Product Mapping.csv'))
    reporting_date = date.today()

    # Tạo output_df để chứa kết quả
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    
    # Tạo cột Reporting_Date
    output_df['Reporting Date'] = pd.Series(np.full(df1['Instrument Id'].shape[0], reporting_date), dtype='datetime64[ns]')
    
    # Format định dạng ngày tháng cho Instrument_Maturity_Date
    valid_dates_df1 = pd.to_datetime(df1['Instrument Maturity Date'], errors='coerce')

    # Loại bỏ các giá trị không hợp lệ
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]

    output_df['Difference'] = valid_dates_df1 - output_df['Reporting Date']
    output_df['Days To Maturity'] = np.where(
        output_df['Difference'].dt.days < 0,
    # Tính Days_To_Maturity
        '30 or Less',
        np.where(output_df['Difference'].dt.days <= 30, '30 or Less', 'More Than 30 Days')
        )   


    output_df['Days To Maturity'] = np.where(
        df1['Instrument Maturity Date'] == 0,
        '30 or Less',
        output_df['Days To Maturity']
        )

    output_df.drop('Difference', axis=1, inplace=True)
    df1['Next Principal Payment Amount'] = df1['Next Principal Payment Amount'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df4_subset = df4.iloc[0:8]  # Subset df4 từ hàng 1 đến hàng 8
    map_dict = df4_subset.set_index('Instruments/Products')['Instruments/Product Type'].to_dict()
    output_df['Mapped Product Type'] = df1['Instrument Type'].map(map_dict)
    
    # Merge df1 và df2
    merged_df = df1.merge(df2[['Counterparty Type', 'Counterparty Category']], 
                          left_on='Customer Type', 
                          right_on='Counterparty Type', 
                          how='left')

    output_df['Counterparty Category'] = merged_df['Counterparty Category']
    
    output_df['Run Off Factor'] = 1

    # Tính Weighted_Principal_Cash_Outflow
    df1['Face Value'] =df1['Face Value'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['Weighted Principal Cash Outflow'] = np.where(
    output_df['Days To Maturity'] == '30 or Less',
    df1['Face Value'] * output_df['Run Off Factor'],
    0
    )

    valid_dates2_df1 = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    valid_rows2_df1 = valid_dates2_df1.notnull()
    valid_dates2_df1 = valid_dates2_df1[valid_rows2_df1]
    
    # Tính Days_To_Coupon
    output_df['Difference2'] = valid_dates2_df1 - output_df['Reporting Date']
    output_df['Days To Coupon'] = np.where(
        output_df['Difference2'].dt.days < 0,
        '30 or Less',
        np.where(output_df['Difference2'].dt.days <= 30, '30 or Less', 'More Than 30 Days')
        )
    
    output_df['Days To Coupon'] = np.where(
        df1['Next Interest Payment Due Date'] == 0,
        '30 or Less',
        output_df['Days To Coupon']
        )

    
    output_df.drop('Difference2', axis=1, inplace=True)
    
        # Tính Weighted_Coupon_Cash_Outflow
    df1['Next Interest Payment Amount'] = df1['Next Interest Payment Amount'].astype(str).str.replace(',', '').astype(float)

    output_df['Weighted Coupon Cash Outflow'] = np.where(
            output_df['Days To Coupon'] == '30 or Less',
            df1['Next Interest Payment Amount'] * output_df['Run Off Factor'],
            0
            )

    # Tính Total_Weighted_Cash_Outflow
    output_df['Weighted Coupon Cash Outflow'] = pd.to_numeric(output_df['Weighted Coupon Cash Outflow'], errors='coerce')
    output_df['Weighted Principal Cash Outflow'] = pd.to_numeric(output_df['Weighted Principal Cash Outflow'], errors='coerce')
    output_df['Total Weighted Cash Outflow'] = output_df['Weighted Coupon Cash Outflow'] + output_df['Weighted Principal Cash Outflow']
    final_output_df = df1.join(output_df)

    return final_output_df

