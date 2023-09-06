"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date
def lcr_offbalancesheet():
    # Reporting date
    reporting_date = date.today()
    path = os.path.dirname(os.path.realpath(__file__))

    df1 = pd.read_csv(os.path.join(path,'input', 'Off Balance Sheet.csv'))
    df2 = pd.read_csv(os.path.join(path, 'input', 'Counterparty Mapping.csv'))
    df3 = pd.read_csv(os.path.join(path, 'input', 'OBS Product Mapping.csv'))
    df4 = pd.read_csv(os.path.join(path, 'input', 'Facility Mapping.csv'))
    
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)
    output_df['Reporting Date'] = pd.Series(np.full(df1['Off BS Account ID'].shape[0], reporting_date), dtype='datetime64[ns]')
    
    # Hợp nhất df1 với df2 dựa trên 'Business entity type' và 'Counterparty Type'
    merged_df = df1.merge(df2[['Counterparty Type', 'Counterparty Category']], 
                          left_on='Business entity type ', 
                          right_on='Counterparty Type', 
                          how='left')
    
    # Điền giá trị 'Corp' vào những chỗ trống trong 'Counterparty Category'
    merged_df['Counterparty Category'].fillna('Corp', inplace=True)
    
    # Tạo cột mới trong output_df
    output_df['Counterparty Category'] = merged_df['Counterparty Category']
    
    # Hợp nhất df1 và df3 dựa trên 'Product Type' và 'Product'
    merged_df = merged_df.merge(df3[['Product', 'Type of Facility']], 
                          left_on='Product Type', 
                          right_on='Product', 
                          how='left')
    
    # Điền giá trị 'Credit' vào những chỗ trống trong 'Type of Facility'
    merged_df['Type of Facility'].fillna('Credit', inplace=True)
    
    # Tạo cột mới trong output_df
    output_df['Type of OBS Items'] = merged_df['Type of Facility']
    
    # Tạo một hàm để áp dụng quy tắc trên Word
    def calculate_runoff_factor(row):
        if row['Type of OBS Items'] == "Trade Finance":
            return 0.05
        else:
            result_1 = df4.loc[df4['Type of Facility'] == row['Type of OBS Items'], 'Run Off Factor']
            if len(result_1) > 0:
                return result_1.values[0]
            else:
                concat_value = row['Type of OBS Items'] + row['Counterparty Category']
                result_2 = df4.loc[df4['CONCAT'] == concat_value, 'Run Off Factor']
                return result_2.values[0] if len(result_2) > 0 else np.nan
    
    # Áp dụng hàm trên cho từng dòng trong dataframe
    output_df['Runoff Factor'] = output_df.apply(calculate_runoff_factor, axis=1)

    df1[' Unutilised Value '] = df1[' Unutilised Value '].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['Cash Outflow'] = output_df['Runoff Factor'] * df1[' Unutilised Value ']
    output_df['Cash Outflow'] = output_df['Cash Outflow'].apply(lambda x: '{:,}'.format(x))
    output_df['Cash Outflow'] = output_df['Cash Outflow'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df = df1.join(output_df)

    return final_output_df
