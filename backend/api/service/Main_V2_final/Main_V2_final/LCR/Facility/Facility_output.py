"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from ...Input_Files import getFiles
from datetime import datetime

def lcr_facility(input_date_str):
    # Reporting date
    reporting_date = datetime.strptime(input_date_str, "%d-%m-%Y")
    input_folder_path = "Facility"
    df1 = getFiles.getFileByName(input_folder_path,  f'Facility_{input_date_str}.csv')
    df2 = getFiles.getFileByName(input_folder_path,  'Counterparty Mapping.csv')
    df3 = getFiles.getFileByName(input_folder_path,  'OBS Product Mapping.csv')
    df4 = getFiles.getFileByName(input_folder_path,  'Facility Mapping.csv')
    df1.fillna(0, inplace=True)

    #output dataframe
    output_df = pd.DataFrame()
    output_df['Reporting Date'] = pd.Series(np.full(df1['Facility ID'].shape[0], reporting_date), dtype='datetime64[ns]')
    
    # Merge df1 và df3 dựa trên cột 'Product Type' và 'Product'
    merged_df = df1.merge(df3[['Product', 'Type of Facility']], 
                          left_on='Product Type', 
                          right_on='Product', 
                          how='left')
    
    # Tạo cột mới 'Credit/Liquid' từ cột 'Type of Facility' của dataframe đã merge
    # Nếu giá trị là NaN (tức là không tìm thấy trong df3), thì thay thế bằng 'Credit'
    output_df['Credit/Liquid'] = merged_df['Type of Facility'].fillna('Credit')
    
    # Merge df1 và df2 dựa trên cột 'Customer Type' và 'Counterparty Type'
    merged_df = df1.merge(df2[['Counterparty Type', 'Counterparty Category']], 
                          left_on='Customer Type', 
                          right_on='Counterparty Type', 
                          how='left')
    
    # Tạo cột mới 'Counterparty Category' trong dataframe output_df từ cột 'Counterparty Category' của merged_df
    output_df['Counterparty Category'] = merged_df['Counterparty Category']
    
    def calculate_runoff_factor(row):
        if row["Credit/Liquid"] == "Trade Finance":
            return df4.loc[df4["Type of Facility"] == row["Credit/Liquid"], "Run Off Factor"].values[0]
        else:
            lookup_value = str(row["Credit/Liquid"]) + str(row["Counterparty Category"])
            filtered_df = df4.loc[df4["CONCAT"] == lookup_value, "Run Off Factor"]
        if not filtered_df.empty:
            return filtered_df.values[0]
        else:
            return None  # hoặc một giá trị mặc định nào đó

    
    # Apply the function to each row in the data
    output_df["Runoff Factor"] = output_df.apply(calculate_runoff_factor, axis=1)
    output_df["Runoff Factor"] = output_df["Runoff Factor"].str.replace('%', '').astype(float) / 100
    df1[' Undrawn Credit Line '] = df1[' Undrawn Credit Line '].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df[' Outflow (undrawn portion resp) '] = output_df["Runoff Factor"] * df1[' Undrawn Credit Line ']

    final_output_df = df1.join(output_df)

    return final_output_df

