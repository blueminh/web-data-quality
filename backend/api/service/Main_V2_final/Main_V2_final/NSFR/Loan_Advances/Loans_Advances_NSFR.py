import numpy as np
import pandas as pd
import os 
from ..Loan_Advances import Loans_Advances
from ..Collateral_for_Loans import Collateral_for_Loans_NSFR

def Loans_Advances_NSFR():
    path = os.path.dirname(os.path.realpath(__file__))
    df1 =  pd.read_csv(os.path.join(path, 'input', 'Loans & Advances.csv'))
    df2 =  Loans_Advances.lcr_Loans_Advances()
    df3 =  Collateral_for_Loans_NSFR.nsfr_collateral()
    df4 =  Collateral_for_Loans_NSFR.get_collateral_for_loans()
    df5 =  pd.read_csv(os.path.join(path, 'input', 'LOANS AND ADVANCES MAPPING.csv'))
    output_df = pd.DataFrame()
    df1.fillna(0, inplace=True)

    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')
    day_diff = (df1['Maturity Date'] - df2['Reporting Date']).dt.days
    
    output_df['Days to Maturity'] = np.where(df1['Maturity Date'].isnull(), 'No Maturity', 
                                         np.where(day_diff > 360, "More than 1 year", 
                                                  np.where(day_diff > 180, "6 months to 1 year", "Less than 6 months")))

# Tạo một DataFrame mới kết hợp df3 và df4
    collateral_for_loans_df = pd.concat([df4[['Loan Id']], df3[['HQLA Asset']]], axis=1)

# Thực hiện phép lookup
    merged_df = pd.merge(df1, collateral_for_loans_df, left_on='Loan Id', right_on='Loan Id', how='left')

# Kiểm tra các giá trị NA và thay thế chúng
    merged_df['HQLA Asset'].fillna('NA', inplace=True)

# Tạo cột mới trong df1 từ kết quả trên
    output_df['Collateral Asset level'] = merged_df['HQLA Asset']


    df1['Risk Weight  as per C41'] = df1['Risk Weight  as per C41'].astype(str).str.rstrip('%').astype('float') / 100.0
    output_df['Risk Weight as per C41'] = df1['Risk Weight  as per C41'].apply(lambda x: '35% or higher' if x > 0.35 else '35% or lower')

    df2['Concat'] = df2['Counterparty Category'].astype(str) + output_df['Days to Maturity'] + output_df['Collateral Asset level'] + output_df['Risk Weight as per C41']

    df5['Concat'] = df5['Concat']

# Thực hiện vlookup bằng cách sử dụng merge
    merged_df = pd.merge(df2, df5, on='Concat', how='left')

    condition = df1['Loan Group'].isin([1, 2])
    output_df['RSF Factor'] = np.where(condition, merged_df['RSF Factor'], "100%")
    output_df['RSF Factor'] =  output_df['RSF Factor'].str.rstrip('%').astype('float') / 100.0

    df1['Loan Outstanding'] = df1['Loan Outstanding'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['Provision'] = df1['Provision'].str.replace(',', '').replace(' -   ', '0').astype(float)
    
    output_df['RSF Amount'] = (output_df['RSF Factor'] * (df1['Loan Outstanding'] - df1['Provision'])).fillna(0)

    output_df['RSF Factor for accrued interest'] = 1
    
    df1['Accrued Interest'] = df1['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    
    output_df['RSF Amount for Accrued Interest'] = output_df['RSF Factor for accrued interest'] * df1['Accrued Interest']
    
    output_df['Total RSF Amount'] = output_df['RSF Amount for Accrued Interest'] + output_df['RSF Amount']
    final_output_df = df2.join(output_df)
    final_output_df = final_output_df.drop('Concat', axis=1)
    final_output_df['Accrued Interest'] = final_output_df['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df['Loan Outstanding'] = final_output_df['Loan Outstanding'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df['Risk Weight  as per C41'] = final_output_df['Risk Weight  as per C41'].str.rstrip('%').astype('float') / 100.0
    return final_output_df
