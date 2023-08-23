"""
@Author: Minh Anh & Gia Hieu
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date
path = os.path.dirname(os.path.realpath(__file__))

def lcr_Loans_Advances(path):
    df1 = pd.read_csv(os.path.join(path,'input', 'Loans & Advances.csv'))
    df2 = pd.read_csv(os.path.join(path,'input', 'CounterParty Mapping.csv'))
    df3 = pd.read_csv(os.path.join(path,'input', 'Cash Inflow Counterparty Mapping.csv'))
    reporting_date = date(2022, 9, 30)


    # Tạo output_df để chứa kết quả
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)

    # Tạo cột Reporting_Date
    output_df['Reporting Date'] = pd.Series(np.full(df1['Loan Id'].shape[0], reporting_date), dtype='datetime64[ns]')
    
    # Merge df2 và df3
    merged_df = df1.merge(df2[['Counterparty Type', 'Counterparty Category']], 
                          left_on='Customer Type', 
                          right_on='Counterparty Type', 
                          how='left')

    # Tạo cột 'Counterparty Category' trong dataframe output_df từ cột 'Counterparty Category' của merged_df
    output_df['Counterparty Category'] = merged_df['Counterparty Category']
    
    output_df['Lookup Result'] = output_df['Counterparty Category'].map(
        dict(zip(df3['Counterparty Category'], df3['Inflow Rate']))
    )
    
    # Apply the conditions from the IF statements in Excel and create the new 'Inflow Rate' column
    output_df['Inflow Rate'] = np.where(
        (df1['Overdue Flag'] == " No ") & (df1['Loan Group'] == 1), output_df['Lookup Result'], 0
    )
    output_df.drop('Lookup Result', axis=1, inplace=True)


    # Format định dạng ngày tháng cho Instrument_Maturity_Date
    valid_dates_df1 = pd.to_datetime(df1['Next Principle Due Date'], errors='coerce')

    # Loại bỏ các giá trị không hợp lệ
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]

    # Tính Days_To_Maturity_For_Principle_Amount
    output_df['Difference'] = valid_dates_df1 - output_df['Reporting Date']
    output_df['Days To Maturity For Principle Amount'] = np.where(
        output_df['Difference'].dt.days < 0,
        '30 or Less',
        np.where(output_df['Difference'].dt.days <= 30, '30 or Less', 'More Than 30 Days')
        )

    output_df['Days To Maturity For Principle Amount'] = np.where(
        df1['Next Principle Due Date'] == 0,
        '30 or Less',
        output_df['Days To Maturity For Principle Amount']
        )

    output_df.drop('Difference', axis=1, inplace=True)
    
    # Tính Installment_Amount_For_Principle_Amount
    output_df['Installment Amount For Principle Amount'] = np.where(
        output_df['Days To Maturity For Principle Amount'] == '30 or Less',
        df1['Principal Repayment'], 0
        )


    # Format định dạng ngày tháng cho Next_Interest_Due_Date
    valid_dates2_df1 = pd.to_datetime(df1['Next Interest Due Date'], errors='coerce')
    
    # Loại bỏ các giá trị không hợp lệ
    valid_rows2_df1 = valid_dates2_df1.notnull()
    valid_dates2_df1 = valid_dates2_df1[valid_rows2_df1]
    
    # Tính Days_To_Maturity_For_Interest_Amount
    output_df['Difference2'] = valid_dates2_df1 - output_df['Reporting Date']
    output_df['Days To Maturity For Interest Amount'] = np.where(
        output_df['Difference2'].dt.days > 30,
        'More Than 30 Days', '30 or Less'
        )

    output_df.drop('Difference2', axis=1, inplace=True)
    
    # Tính Installment_Amount_For_Interest_Amount
    df1['Interest Payment'] = pd.to_numeric(df1['Interest Payment'].str.replace(',', '').replace(' -   ', '0'), errors='coerce')
    output_df['Installment Amount For Interest Amount'] = np.where(
        output_df['Days To Maturity For Interest Amount'] == '30 or Less',
        df1['Interest Payment'], 0
        )
    

    # Tính Total_Unweighted_Inflows
    # Chuyển đổi cả hai cột thành dạng số, chuyển đổi giá trị trống thành NaN

    output_df['Installment Amount For Interest Amount'] = pd.to_numeric(output_df['Installment Amount For Interest Amount'].astype(str).str.replace(',', '').replace(' -   ', '0'), errors='coerce')

    output_df['Installment Amount For Principle Amount'] = pd.to_numeric(output_df['Installment Amount For Principle Amount'].str.replace(',', '').replace(' -   ', '0'), errors='coerce')
    
    # Tính 'Total Unweighted Inflows' với điều kiện ban đầu
    output_df['Total Unweighted Inflows'] = np.where(
        pd.isna(output_df['Installment Amount For Interest Amount']),
        0,  
        output_df['Installment Amount For Interest Amount'] + output_df['Installment Amount For Principle Amount']
    )
    
    # Thêm điều kiện mới: nếu 'Installment Amount For Principle Amount' bị trống, 
    # thì 'Total Unweighted Inflows' sẽ bằng 'Installment Amount For Interest Amount'
    output_df.loc[pd.isna(output_df['Installment Amount For Principle Amount']), 'Total Unweighted Inflows'] = output_df['Installment Amount For Interest Amount']

    # Tính Weighted_Inflows
    output_df['Inflow Rate'] = output_df['Inflow Rate'].str.rstrip('%').astype('float') / 100.0

    output_df['Inflow Rate'] = output_df['Inflow Rate'].fillna(0)

    output_df['Weighted Inflows'] = output_df['Inflow Rate']*output_df['Total Unweighted Inflows']
    
    final_output_df = df1.join(output_df)
    
    
    return final_output_df


final_output_df = lcr_Loans_Advances(path)




