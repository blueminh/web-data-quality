"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date

path = os.path.dirname(os.path.realpath(__file__))

# Reporting date

def lcr_investmentandtradingsecurities(path):
    df1 = pd.read_csv(os.path.join(path, 'input', 'Investment&Trading Securities.csv'))
    df2 = pd.read_csv(os.path.join(path, 'input', 'Asset Issuers HQLA Mapping.csv'))
    df3 = pd.read_csv(os.path.join(path, 'input', 'Product Mapping.csv'))
    df4 = pd.read_csv(os.path.join(path, 'input', 'Counterparty Mapping.csv'))
    df5 = pd.read_csv(os.path.join(path, 'input', 'Currency table regulatry.csv'))
    df6 = pd.read_csv(os.path.join(path, 'input', 'Risk Weight Table.csv'))
    df7 = pd.read_csv(os.path.join(path, 'input', 'Rating Table.csv'))
    df8 = pd.read_csv(os.path.join(path, 'input', 'HQLA asset table.csv'))
    df9 = pd.read_csv(os.path.join(path, 'input', 'HQLA weight table.csv'))
    df10 = pd.read_csv(os.path.join(path, 'input', 'Cash Inflow Counterparty Mapping.csv'))
    reporting_date = date.today()

    df1.fillna(0, inplace=True)
    output_df = pd.DataFrame()
    output_df.fillna(0, inplace=True)

    output_df['Reporting Date'] = pd.Series(np.full(df1['Instrument Type'].shape[0], reporting_date), dtype='datetime64[ns]')
    df1['Pledged amount used for liquidity'] = df1['Pledged amount used for liquidity'].str.replace(',', '').astype(float)
    df1['Market Value'] = df1['Market Value'].str.replace(',', '').astype(float)
    output_df['Pledged amount not used for liquidity'] = np.where(df1['Market Value'].isna(), 0, df1['Market Value']) - df1['Pledged amount used for liquidity'].fillna(0)
    
    # Thay thế các giá trị NaN bằng 0 trong df2
    df2.fillna(0, inplace=True)
    
    # Tạo dict để ánh xạ giữa giá trị cần thay thế và giá trị mới từ df2
    mapping_dict = dict(zip(df2['Pledged to institition'], df2['HQLA']))
    
    # Thay thế giá trị trong cột 'Pledged to other institute' bằng giá trị tương ứng từ dict mapping_dict
    output_df['Included in HQLA'] = df1['Pledged to other institute'].map(mapping_dict)
    
    # Thay thế giá trị 'NA' trong cột 'Included in HQLA' bằng giá trị 'NA'
    output_df['Included in HQLA'] = np.where(output_df['Included in HQLA'] == 'NA', 'NA', output_df['Included in HQLA'])
    
    # Thay thế giá trị 0 bằng 'NA'
    output_df['Included in HQLA'] = output_df['Included in HQLA'].replace(0, 'NA')
    
    valid_dates_df1 = pd.to_datetime(df1['Instrument Maturity Date'], errors='coerce')
    output_df['Days To Maturity'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less'
    )
    output_df.loc[df1['Instrument Maturity Date'] == 0,'Days To Maturity'] = '30 or Less'
    
    output_df['Mapped Product Type'] = df1['Instrument Type'].map(df3.head(8).set_index('Instruments/Products')['Instruments/Product Type'])
    
    merged_df = df1.merge(df4, how='left', left_on='Issuer Counterparty Type', right_on='Counterparty Type')
    output_df['Counterparty Category'] = merged_df['Counterparty Category']
    
    merged_df = df1.merge(df5[["ISO Code", "Currency Flag"]], left_on="Currency", right_on="ISO Code", how="left")
    output_df["Currency Flag"] = merged_df["Currency Flag"]
    
    merged_df = df1.merge(df6[["Risk Weight", "HQLA Asset"]], left_on="Risk Weight As Per C41", right_on="Risk Weight", how="left")
    output_df['Risk Weight Category'] = merged_df["HQLA Asset"]
    
    df1["Concat"] = df1["Rating Agency"] + df1["Credit Rating"]
    
    merged_df = df1.merge(df7[["Concat", "RATING CD"]], on="Concat", how="outer")
    
    merged_df["RATING CD"].fillna("LOW", inplace=True)
    
    output_df["Rating CD"] = merged_df["RATING CD"]
    
    # Tạo cột "Market Value" trong output_df từ cột "Market Value" của df1
    output_df["Market value"] = df1["Market Value"]
    output_df["Concat"] = output_df["Mapped Product Type"] + output_df["Counterparty Category"] + output_df["Currency Flag"] + output_df["Risk Weight Category"] + output_df["Rating CD"]
    
    output_df["HQLA Asset"] = np.where(output_df["Market value"] != 0, output_df["Concat"].map(df8.set_index("CONCAT")["HQLA Asset"]), "NA")
    
    # Chèn "NA" vào những ô bị thiếu trong cột "HQLA Asset"
    output_df["HQLA Asset"].fillna("NA", inplace=True)
    
    # Xóa cột "Concat" để làm sạch dataframe output_df
    output_df.drop("Concat", axis=1, inplace=True) 
    
    # Tạo cột "concat" trong output_df
    output_df["concat"] = output_df["HQLA Asset"] + output_df["Mapped Product Type"]
    
    # Tạo cột "Weight" trong output_df
    output_df["Weight"] = np.where(output_df["Included in HQLA"] == "HQLA", output_df["concat"].map(df9.set_index("Concat")["Weight"]), "NA")
    def convert_to_float(x):
        if isinstance(x, str):
            if x != 'NA':
                return float(x.strip('%')) / 100
            else:
                return 'NA'
        else:
            return x


    output_df["Weight"] = output_df["Weight"].apply(convert_to_float)


    
    # Xóa cột "Concat" để làm sạch dataframe output_df
    output_df.drop("concat", axis=1, inplace=True) 
    
    # Tạo cột "Unweighted market value amount" trong output_df
    output_df["Unweighted Market Value Amount"] = output_df.apply(lambda column: 0 if column["Weight"] == "NA" else column["Pledged amount not used for liquidity"], axis=1)
    
    #Tạo cột Weighted Amount for HQLA
    def calculate_weighted_amount(column):
        weight = column["Weight"]
        market_value = column["Unweighted Market Value Amount"]
        
        if weight == "NA":
            return ""
        else:
            return market_value * weight
        
    output_df["Weighted Amount for HQLA"] = output_df.apply(calculate_weighted_amount, axis=1)
    
    
    # Sử dụng np.where để tạo cột mới dựa trên điều kiện
    output_df['Unweighted Principal Cash Inflow'] = np.where(
        output_df['Days To Maturity'] == '30 or Less',
        np.where(df1['Market Value'] == 0, df1['Book Value'], df1['Market Value']),
        0
    )
    
    df1['Next Coupon Date'] = pd.to_datetime(df1['Next Coupon Date'], errors='coerce')
    output_df['Days To Coupon'] = np.where(
        pd.to_datetime(df1['Next Coupon Date'], errors='coerce').isna(),
        'No Coupon/Dividend',
        np.where((pd.to_datetime(df1['Next Coupon Date'], errors='coerce') - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less')
    )

    # Merge hai dataframe
    output_df = pd.merge(output_df, df10[['Counterparty Category', 'Inflow Rate']], 
                         on='Counterparty Category', 
                         how='left')
    # Đổi tên cột
    output_df = output_df.rename(columns={'Inflow Rate': 'Inflow Factor'})
    
    
    output_df['Coupon Cash Inflow'] = np.where(output_df['Days To Coupon'] == "30 or Less", df1['Next Interest Payment Amount'], 0)
    
    # Chuyển đổi cột 'Coupon Cash Inflow' sang số thực
    output_df['Coupon Cash Inflow'] = pd.to_numeric(output_df['Coupon Cash Inflow'], errors='coerce')
    output_df['Inflow Factor'] = output_df['Inflow Factor'].str.rstrip('%').astype('float') / 100.0
    # Thực hiện phép nhân
    output_df['Weighted Coupon cash inflow'] = output_df['Inflow Factor'] * output_df['Coupon Cash Inflow']
    
    
    output_df['Unweighted Principal Cash Inflow'] = pd.to_numeric(output_df['Unweighted Principal Cash Inflow'], errors='coerce')
    output_df['Weighted Princial Cash Inflow'] = output_df['Inflow Factor'] * output_df['Unweighted Principal Cash Inflow']
    
    output_df.drop("Market value", axis=1, inplace=True) 
    final_output_df = df1.join(output_df)

    return final_output_df

final_output_df = lcr_investmentandtradingsecurities(path)



