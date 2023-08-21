"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date
path = os.path.dirname(os.path.realpath(__file__))

def nsfr_collateral(path):
    # Reporting date
    reporting_date = date.today()

    df1 =  pd.read_csv(os.path.join(path, 'input', 'Collateral for Loans.csv'))
    df2 =  pd.read_csv(os.path.join(path, 'input', 'Collateral Product Mapping.csv'))
    df3 =  pd.read_csv(os.path.join(path, 'input', 'Counterparty Mapping.csv'))
    df4 =  pd.read_csv(os.path.join(path, 'input', 'Currency table regulatry.csv'))
    df5 =  pd.read_csv(os.path.join(path, 'input', 'Risk Weight Table.csv'))
    df6 =  pd.read_csv(os.path.join(path, 'input', 'Rating Table.csv'))
    df7 =  pd.read_csv(os.path.join(path, 'input', 'HQLA asset table.csv'))

    df1.fillna(0, inplace=True)
    output_df = pd.DataFrame()
    output_df.fillna(0, inplace=True)

    output_df['Reporting Date'] = pd.Series(np.full(df1['Loan Id'].shape[0], reporting_date), dtype='datetime64[ns]')


    df_merged = pd.merge(df1, df2, left_on='Diễn giải (Bổ sung thêm 1 cột)', right_on='Instruments/Products', how='left')
    output_df['Mapped Product Type'] = df_merged['Instruments/Product Type']

    df_merged = pd.merge(df1, df3, left_on='Customer Type', right_on='Counterparty Type', how='left')
    output_df['Counterparty Category'] = df_merged['Counterparty Category']

    df_merged = pd.merge(df1, df4, left_on='Currency', right_on='ISO Code', how='left')
    output_df['Currency Flag'] = df_merged['Currency Flag']

    df_merged = pd.merge(df1, df5, left_on='Risk Weight As Per C41', right_on='Risk Weight', how='left')
    output_df['Risk Weight Category'] = df_merged['HQLA Asset']

    df1["Credit Agency"] = df1["Credit Agency"].astype(str)
    df1["Rating"] = df1["Rating"].astype(str)
    df1["Concat"] = df1["Credit Agency"] + df1["Rating"]

    merged_df = df1.merge(df6[["Concat", "RATING_CD"]], on="Concat", how="outer")

    merged_df["RATING_CD"].fillna("LOW", inplace=True)

    output_df["Rating CD"] = merged_df["RATING_CD"]

    output_df['Mapped Product Type'] = output_df['Mapped Product Type'].astype(str)
    output_df['Counterparty Category'] = output_df['Counterparty Category'].astype(str)
    output_df['Currency Flag'] = output_df['Currency Flag'].astype(str)
    output_df['Risk Weight Category'] = output_df['Risk Weight Category'].astype(str)
    output_df['Rating CD'] = output_df['Rating CD'].astype(str)
    df7['CONCAT'] = df7['CONCAT'].astype(str)

    output_df['combined'] = output_df['Mapped Product Type'] + output_df['Counterparty Category'] + output_df['Currency Flag'] + output_df['Risk Weight Category'] + output_df['Rating CD']
    df7['combined'] = df7['CONCAT']

    merged_df = pd.merge(output_df, df7, on='combined', how='outer')
    output_df['HQLA Asset'] = merged_df['HQLA Asset']
    output_df.drop('combined', axis=1, inplace=True)
    # Concatenate df1 and output_df along the column axis.
    final_output_df = df1.join(output_df)
    final_output_df = final_output_df.drop('Concat', axis =1)
    final_output_df['Risk Weight As Per C41'] = final_output_df['Risk Weight As Per C41'].str.rstrip('%').astype('float') / 100.0
    final_output_df['Collateral Amount'] =   final_output_df['Collateral Amount'].str.replace(',', '').astype(float)
    final_output_df['Loan secured amount'] =   final_output_df['Loan secured amount'].str.replace(',', '').astype(float)
    return final_output_df


final_output_df = nsfr_collateral(path)

