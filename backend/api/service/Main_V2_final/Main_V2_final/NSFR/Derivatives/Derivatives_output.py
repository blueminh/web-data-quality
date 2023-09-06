"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date

def lcr_derivatives():
    path = os.path.dirname(os.path.realpath(__file__))
    reporting_date = date.today()

    df1 = pd.read_csv(os.path.join(path, 'input', 'Derivatives.csv'))
    
    output_df = pd.DataFrame()
    
    output_df['Reporting Date'] = pd.Series(np.full(df1['Deal No'].shape[0], reporting_date), dtype='datetime64[ns]')
    
    valid_dates_df1 = pd.to_datetime(df1['End Date'], errors='coerce')
    
    # Lọc bỏ các giá trị không hợp lệ
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]
    
    output_df['Difference'] = valid_dates_df1 - output_df['Reporting Date']
    output_df['Days to Maturity'] = np.where(
        output_df['Difference'].dt.days < 0,
        '30 or Less',
        np.where(output_df['Difference'].dt.days <= 30, '30 or Less', 'More Than 30 Days')
    )
    
    output_df.drop('Difference', axis=1, inplace=True)
    df1['MTM'] = df1['MTM'].str.replace(',', '')
    df1['MTM'] = df1['MTM'].apply(lambda x: float(x.replace('(', '-').replace(')', '')) if isinstance(x, str) else x)

    # Tạo cột mới 'Inflow Amount'
    output_df['Inflow Amount'] = np.where((output_df['Days to Maturity'] == '30 or Less') & (df1['MTM'] > 0), df1['MTM'], 0)
    
    # Tạo cột mới 'Outflow Amount'
    output_df['Outflow Amount'] = np.where((output_df['Days to Maturity'] == '30 or Less') & (df1['MTM'] < 0), df1['MTM'], 0)



    
    final_output_df = df1.join(output_df)
    return final_output_df