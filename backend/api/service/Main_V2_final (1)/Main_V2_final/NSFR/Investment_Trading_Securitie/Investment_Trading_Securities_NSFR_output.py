import pandas as pd
import numpy as np
import os
from .Investment_Trading_Securities import Investment_Trading_Securities_output

# Đường dẫn đến file
path = os.path.dirname(os.path.realpath(__file__))
def nsfr_investmentandtradingsecurities(path, input_date_str):
    invest = f"Investment&Trading Securities_{input_date_str}.csv"
    # Reporting date

    
    df1 = pd.read_csv(os.path.join(path, 'Investment_Trading_Securities', 'input', invest))
    df2 = pd.read_csv(os.path.join(path, 'Investment_Trading_Securities', 'input', 'INVESTMENT SECURITIES MAPPING (used).csv'))
    df3 = Investment_Trading_Securities_output.lcr_investmentandtradingsecurities(os.path.join(path, 'Investment_Trading_Securities'))
    
    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()
    
    output_df['Encumbered/Unencumbered Status'] = np.where(df1['Pledged to other institute'] == 0, 'Unencumbered', 'Encumbered')
    

    
    valid_dates_df1 = pd.to_datetime(df1['Instrument Maturity Date'], errors='coerce')
    df3['Reporting Date'] = pd.to_datetime(df3['Reporting Date'])

    # Tính số ngày từ 'Reporting Date' đến 'Instrument Maturity Date', và bỏ qua các dòng không hợp lệ
    output_df['Days to maturity'] = (valid_dates_df1 - df3['Reporting Date']).dt.days
    
    
    conditions = [
        output_df['Days to maturity'] < 0,
        (output_df['Days to maturity'] >= 0) & (output_df['Days to maturity'] <180),
        output_df['Days to maturity'] >= 360
        ]
    
    choices = [
        'No Maturity',
        'Less than 6 months',
        'More than 1 year'
        ]
    
    
    output_df['Instrument Maturity bucket'] = np.select(conditions, choices, default = '6 months to 1 year')
    
    
    # Chuyển đổi cột 'Encumbered End Date' và 'Instrument Maturity Date' sang định dạng pandas Timestamp
    df1['Encumbered End Date'] = pd.to_datetime(df1['Encumbered End Date'], errors='coerce')
    df1['Instrument Maturity Date'] = pd.to_datetime(df1['Instrument Maturity Date'], errors='coerce')
    df1['Next Coupon Date'] = pd.to_datetime(df1['Next Coupon Date'], errors='coerce')
    
    # Tính số ngày từ 'Reporting Date' đến 'Encumbered End Date' hoặc 'Instrument Maturity Date'
    df1['Days'] = np.where(df1['Encumbered End Date'].isna(), (df1['Instrument Maturity Date'] - df3['Reporting Date']).dt.days, (df1['Encumbered End Date'] - df3['Reporting Date']).dt.days)
    
    # Tạo cột mới 'Encumbered Period' trong dataframe output_df
    output_df['Encumbered Period'] = np.where(
        output_df['Encumbered/Unencumbered Status'] == 'Unencumbered', 
        'None',
        np.where(
            df1['Days'] < 0, 
            'No Maturity', 
            np.where(
                df1['Days'] >= 360, 
                'More than 1 year',
                np.where(
                    df1['Days'] < 180, 
                    'Less than 6 months', 
                    '6 months to 1 year'
                )
            )
        )
    )
    # Chèn "NA" vào những ô bị thiếu trong cột "HQLA Asset"
    df3["HQLA Asset"].fillna("NA", inplace=True)
    df3['Included in HQLA'].fillna("NA", inplace=True)
    
    # Tạo cột "Concat" trong output_df
    output_df['Concat'] = df3['Mapped Product Type'] + df3['Counterparty Category'] + df3['HQLA Asset'] + output_df['Instrument Maturity bucket']
    
    # Ánh xạ giá trị từ df2 vào output_df
    output_df['Unencumbered RSF Factor'] = output_df['Concat'].map(df2.set_index('Concat')['RSF Factor'])
    output_df['Unencumbered RSF Factor'] = output_df['Unencumbered RSF Factor'].str.rstrip('%').astype('float') / 100.0
    
    # Tạo cột mới "Encumbered RSF Factor" trong output_df
    output_df['Encumbered RSF Factor'] = np.where(output_df['Encumbered Period'] == "None", output_df['Unencumbered RSF Factor'],
                                                 np.where(output_df['Encumbered Period'] == "Less than 6 months", output_df['Unencumbered RSF Factor'],
                                                          np.where(output_df['Encumbered Period'] == "6 months to 1 year", output_df['Unencumbered RSF Factor'].max() * 0.5,
                                                                   np.where(output_df['Encumbered Period'] == "More than 1 year", 1,
                                                                            np.where(output_df['Encumbered Period'] == "No Maturity", 1, 0)
                                                                           )
                                                                  )
                                                         )
                                                )
    
    # Tạo cột mới "RSF Amount" trong output_df

    df1['Book Value'] =df1['Book Value'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['Provision'] =df1['Provision'].str.replace(',', '').replace(' -   ', '0').astype(float)

    output_df['RSF Amount'] = np.where(output_df['Encumbered/Unencumbered Status'] == "Unencumbered", output_df['Unencumbered RSF Factor'] * (df1['Book Value'] - df1['Provision']),
                                       output_df['Encumbered RSF Factor'] * (df1['Book Value'] - df1['Provision']))
    
    # Tạo cột mới "Maturity Bucket for Accrued Interest" trong output_df
    output_df['Maturity Bucket for Accrued Interest'] = np.where((df1['Next Coupon Date'] - df3['Reporting Date']).dt.days >= 360, "More than 1 year",
                                                                 np.where((df1['Next Coupon Date'] - df3['Reporting Date']).dt.days >= 180, "6 months to 1 year",
                                                                          "Less than 6 months"))
    
    output_df['RSF factor for Accrued Interest'] = 1
    df1['Accrued Interest'] =df1['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['RSF Amount for Accrued Interest'] = df1['Accrued Interest'] * output_df['RSF factor for Accrued Interest']
    
    output_df['Total RSF Amount'] = output_df['RSF Amount for Accrued Interest'] + output_df['RSF Amount']
    
    
    output_df.fillna(0, inplace=True)
    
    
    output_df.drop("Concat", axis=1, inplace=True) 

    
    final_output_df = df3.join(output_df)
    final_output_df['Book Value'] =final_output_df['Book Value'].str.replace(',', '').astype(float)
    final_output_df['Accrued Interest'] =final_output_df['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df = final_output_df.drop('Concat', axis=1)
    
    
    
    return final_output_df
#output file

final_output_df = nsfr_investmentandtradingsecurities(path, "28-08-2023")
