"""
@Author: Minh Anh
@Status: Completed
"""
import os 
import pandas as pd
import numpy as np
from datetime import date

# Đường dẫn đến file

def lcr_securitiesfinancialtrans():
    # Reporting date
    path = os.path.dirname(os.path.realpath(__file__))
    reporting_date = date.today()
    df1 = pd.read_csv(os.path.join(path, 'input', 'Securities Financial Trans.csv'))
    df2 = pd.read_csv(os.path.join(path, 'input', 'Product Mapping.csv'))
    df3 = pd.read_csv(os.path.join(path, 'input', 'Counterparty Mapping.csv'))
    df4 = pd.read_csv(os.path.join(path, 'input', 'Currency table regulatry.csv'))
    df5 = pd.read_csv(os.path.join(path, 'input', 'Risk Weight Table.csv'))
    df6 = pd.read_csv(os.path.join(path, 'input', 'Rating Table.csv'))
    df7 = pd.read_csv(os.path.join(path, 'input', 'HQLA asset table.csv'))
    df8 = pd.read_csv(os.path.join(path, 'input', 'sft inflow table.csv'))
    df9 = pd.read_csv(os.path.join(path, 'input', 'sft outflow table.csv'))

    df1.fillna(0, inplace=True)

    output_df = pd.DataFrame()
    

    output_df['Reporting Date'] = pd.Series(np.full(df1['Transaction ID'].shape[0], reporting_date), dtype='datetime64[ns]')


    # Chuyển đổi định dạng ngày tháng trong df1
    valid_dates_df1 = pd.to_datetime(df1['Next Principal Payment Due Date'], errors='coerce')

    # Lọc bỏ các giá trị không hợp lệ trong df1
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]

    output_df['Days To Next Principal Payment'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days  <= 30, '30 or Less', 'More Than 30 Days')

    # Kiểm tra và gán giá trị "30 or Less" cho những ô trống của cột 'Days To Next Principal Payment'
    output_df.loc[df1['Next Principal Payment Due Date'] == 0, 'Days To Next Principal Payment'] = '30 or Less'

    # Chuyển đổi định dạng ngày tháng trong df1
    valid_dates_df1 = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')

    # Lọc bỏ các giá trị không hợp lệ trong df1
    valid_rows_df1 = valid_dates_df1.notnull()
    valid_dates_df1 = valid_dates_df1[valid_rows_df1]

    output_df['Days to Interest Payment'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days  <= 30, '30 or Less', 'More Than 30 Days')

    # Kiểm tra và gán giá trị "30 or Less" cho những ô trống của cột 'Days To Next Principal Payment'
    output_df.loc[df1['Next Interest Payment Due Date'] == 0, 'Days To Next Principal Payment'] = '30 or Less'

    # Map transaction type
    merged_df = df1.merge(df2.loc[49:60, ['Instruments/Products', 'Instruments/Product Type']], left_on='Transaction Type', right_on='Instruments/Products', how='left')
    output_df['Transaction type'] = merged_df['Instruments/Product Type']

    # Map underlying asset product type
    merged_df = df1.merge(df2.loc[1:7, ['Instruments/Products', 'Instruments/Product Type']], left_on='Underlying Asset Type', right_on='Instruments/Products', how='left')
    output_df['Underlying Asset Product Type'] = merged_df['Instruments/Product Type']

    # Map underlying asset counterparty
    merged_df = df1.merge(df3, left_on='Underlying Asset Issuer Type', right_on='Counterparty Type', how='left')
    output_df['Underlying Asset Counterparty'] = merged_df['Counterparty Category']

    # Map currency flag
    merged_df = df1.merge(df4, left_on='Currency', right_on='ISO Code', how='left')
    output_df['Currency Flag'] = merged_df['Currency Flag']

    # Thực hiện merge giữa df1 và df5 dựa trên cột 'Underlying Asset Issuer C41 Risk Weight' và 'Risk Weight'
    merged_df = df1.merge(df5[['Risk Weight', 'HQLA Asset']], 
                        left_on='Underlying Asset Issuer C41 Risk Weight', 
                        right_on='Risk Weight', 
                        how='left')

    # Tạo cột mới 'Risk Weight Category' từ cột 'HQLA Asset' của dataframe đã merge
    output_df['Risk Weight Category'] = merged_df['HQLA Asset']

    # Đảm bảo cả hai cột đều có cùng kiểu dữ liệu trước khi hợp nhất
    df1["Concat"] = df1["Credit Agency"].astype(str) + df1["Underlying Asset Rating"].astype((str))
    df6["Concat"] = df6["Concat"].astype(str)

    merged_df = df1.merge(df6[["Concat", "RATING CD"]], on="Concat", how="outer")
    merged_df["RATING CD"].fillna("LOW", inplace=True)
    output_df["Rating CD"] = merged_df["RATING CD"]

    # Tạo cột Concat trong output_df và df7
    output_df["Concat"] = output_df["Underlying Asset Product Type"] + output_df["Underlying Asset Counterparty"] + output_df["Currency Flag"] + output_df["Risk Weight Category"] + output_df["Rating CD"]
    df7["Concat"] = df7["CONCAT"]

    # Thực hiện phép hợp nhất
    merged_df = output_df.merge(df7[["Concat", "HQLA Asset"]], on="Concat", how="left")

    # Đặt cột mới HQLA Asset trong output_df
    output_df["HQLA Asset"] = merged_df["HQLA Asset"]

    # Xóa cột "Concat" để làm sạch dataframe output_df
    output_df.drop("Concat", axis=1, inplace=True) 

    # Merge df1 và df3 dựa trên cột 'Customer Type' và 'Counterparty Type'
    merged_df = df1.merge(df3[['Counterparty Type', 'Counterparty Category']], 
                        left_on='Customer Type', 
                        right_on='Counterparty Type', 
                        how='left')

    # Tạo cột mới 'Counterparty Category' trong dataframe output_df từ cột 'Counterparty Category' của merged_df
    output_df['Counterparty Category'] = merged_df['Counterparty Category']

    # Tạo một cột Concat trong df1 và df8 để thực hiện việc hợp nhất
    df1['Concat'] = df1['Used to cover short position'] + output_df['Transaction type'] + output_df['HQLA Asset']
    df8['Concat'] = df8['CONCAT']

    # Thực hiện hợp nhất giữa df1 và df8
    merged_df = df1.merge(df8[['Concat', 'Inflow %']], on='Concat', how='left')

    # Tạo cột 'Inflow Rate' trong output_df dựa trên cột 'Inflow %' của merged_df và điều kiện
    merged_df = merged_df.reindex(output_df.index)

    output_df['Inflow Rate'] = np.where(
        output_df['Transaction type'] == 'Secured Lending',
        merged_df['Inflow %'],
        0
    )

    # Tính toán giá trị cho cột mới 'Cash Inflow'
    df1['Next Principal Payment Amount'] =df1['Next Principal Payment Amount'].str.replace(',', '').replace(' -   ', '0').astype(float)

    output_df['Cash Inflow'] = np.where(output_df['Days To Next Principal Payment'] == '30 or Less', df1['Next Principal Payment Amount'] * output_df['Inflow Rate'], 0) + np.where(output_df['Days to Interest Payment'] == '30 or Less', df1['Next Interest Payment'] * output_df['Inflow Rate'], 0)

    # Chuyển đổi các giá trị NA thành 0
    output_df['Cash Inflow'] = output_df['Cash Inflow'].fillna(0)

    # Tạo cột "Concat" trong output_df và df9
    output_df["Concat"] = output_df["Transaction type"] + output_df["Counterparty Category"] + output_df["HQLA Asset"] + output_df["Risk Weight Category"]
    df9["Concat"] = df9["CONCAT"]

    # Merge output_df và df9
    merged_df = output_df.merge(df9[['Concat', 'Outflow %']], on="Concat", how="left")

    # Tạo cột mới "RunOff Factor"
    merged_df["RunOff Factor"] = np.where(merged_df['Transaction type'] == 'Secured Borrowing', merged_df['Outflow %'], 0)

    # Sử dụng merged_df thay vì output_df sau này
    output_df = merged_df

    # Xóa cột "Concat"
    output_df.drop('Concat', axis=1, inplace=True)

    # Tính toán giá trị cho cột mới 'Cash Outflow'
    output_df['Cash Outflow'] = np.where(output_df['Days To Next Principal Payment'] == '30 or Less', df1['Next Principal Payment Amount'] * output_df['Inflow Rate'], 0) + np.where(output_df['Days to Interest Payment'] == '30 or Less', df1['Next Interest Payment'] * output_df['Inflow Rate'], 0)

    # Chuyển đổi các giá trị NA thành 0
    output_df['Cash Outflow'] = output_df['Cash Outflow'].fillna(0)

    output_df.drop('Outflow %', axis=1, inplace=True)
    final_output_df = df1.join(output_df)

    return final_output_df


