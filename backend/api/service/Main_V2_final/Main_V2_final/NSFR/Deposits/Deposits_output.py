"""
@Author: Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from datetime import date
from ..Loan_Advances import Loans_Advances


def Deposits_LCR():
    path = os.path.dirname(os.path.realpath(__file__))
    df1 = pd.read_csv(os.path.join(path, 'input', 'Deposit.csv'))
    df2 = pd.read_csv(os.path.join(path, 'input', 'Currency table regulatry.csv'))
    df3 = pd.read_csv(os.path.join(path, 'input', 'CounterParty Mapping.csv'))
    df5 = pd.read_csv(os.path.join(path, 'input', 'insurance table.csv'))
    df6 = Loans_Advances.lcr_Loans_Advances() # Assuming Loans_Advances is a module
    df7 = pd.read_csv(os.path.join(path, 'input', 'Loans & Advances.csv'))
    df8 = pd.read_csv(os.path.join(path, 'input', 'Product Mapping.csv'))
    df9 = pd.read_csv(os.path.join(path, 'input', 'unstable deposit run-off factor table.csv'))
    
    # Tạo output_df để chứa kết quả
    output_df = pd.DataFrame()
    reporting_date = date.today()

    df1.fillna(0, inplace=True)
    
    #reporting date
    output_df['Reporting Date'] = pd.Series(np.full(df1['Account ID'].shape[0], reporting_date), dtype='datetime64[ns]')
 
    #Days to Maturity
    valid_dates_df1 = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    output_df['Days To Maturity'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less'
    )
    output_df.loc[df1['Maturity Date'] == 0,'Days To Maturity'] = '30 or Less'
    
    #Days till next interet payment
    valid_dates_df1 = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    output_df['Days till next interet payment'] = np.where(
        (valid_dates_df1 - output_df['Reporting Date']).dt.days > 30, 
        'More Than 30 Days', 
        '30 or Less'
    )
    output_df.loc[df1['Next Interest Payment Due Date'] == 0,'Days To Maturity'] = '30 or Less'
    
    #Product Type
    df_merged = pd.merge(df1, df8, left_on='Product Type', right_on='Instruments/Products', how='left')
    output_df['Product type'] = df_merged['Instruments/Product Type']
    
    #Retail/Wholesale
    df_merged = pd.merge(df1, df3, left_on='Customer Type', right_on='Counterparty Type', how='left')
    output_df['Retail/Wholesale'] = df_merged['Counterparty Category']
    
    #Currency Flag
    df_merged = pd.merge(df1, df2, left_on='Currency', right_on='ISO Code', how='left')
    output_df['Currency Flag'] = df_merged['Currency Flag']
    
    #Volatile Flag
    output_df['Volatile Flag'] = np.where(output_df['Currency Flag'] == 'Domestic Currency', 'No', 'Yes')
    
    #Insurer Name
    insurer_lookup = df5.set_index('Counterparty Category')['Insurer Name'].to_dict()
    output_df['Insurer Name'] = np.where(
        (output_df['Currency Flag'] == 'Domestic Currency') & (output_df['Retail/Wholesale'] != 'NA'),
        output_df['Retail/Wholesale'].map(insurer_lookup),
        'NA'
    )
    
    # Insured Amount/Customer 
    insured_amount_lookup = df5.set_index('Insurer Name')['Insured Amount'].to_dict()
    output_df['Insured Amount/Customer'] = output_df['Insurer Name'].map(insured_amount_lookup).fillna(0)
    
    # Exclusion Flag for Pledged to Loans 
    df_merged = pd.merge(df1, df7, left_on="Pledged for which loan", right_on="Loan Id", how='left')
    df_merged['Days To Maturity For Principle Amount'] = df6['Days To Maturity For Principle Amount'].astype(str)
    
    conditions = [
        (df_merged['Pledged against a Loan'] == "No"),
        (df_merged['Legal Right to Withdraw?'] == "Yes"),
        (df_merged['Days To Maturity For Principle Amount'] == "30 or Less")
    ]
    
    choices = ["No", "No", "No"]
    
    df_merged['Exclusion Flag for Pledged to Loans'] = np.select(conditions, choices, default="Yes")
    
    output_df['Exclusion Flag for Pledged to Loans'] = df_merged['Exclusion Flag for Pledged to Loans']

    

    # Clean and convert data
    df1['Deposit balance'] = df1['Deposit balance'].str.replace(',', '').astype(float)
    df1['Interest Payable'] = df1['Interest Payable'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['Insured Amount/Customer'] = output_df['Insured Amount/Customer'].str.replace(',', '').astype(float)
    
    # Define conditions
    is_not_pledged = (output_df['Exclusion Flag for Pledged to Loans'] == "No")
    is_not_volatile = (output_df['Volatile Flag'] == "No")
    is_short_term = (output_df['Days To Maturity'] == "30 or Less")
    
    # Calculate sums
    sum_no_volatile = df1.loc[is_not_volatile.values, 'Deposit balance'].groupby(df1.loc[is_not_volatile.values, 'Customer ID']).transform('sum') + df1.loc[(is_not_volatile & is_short_term).values, 'Interest Payable'].groupby(df1.loc[(is_not_volatile & is_short_term).values, 'Customer ID']).transform('sum')
    deposit_plus_interest = df1['Deposit balance'] + df1.loc[is_short_term.values, 'Interest Payable']
    
    # Calculate insured fraction
    insured_fraction = (deposit_plus_interest / sum_no_volatile) * output_df['Insured Amount/Customer']
    
    # Calculate stable amount
    stable_amount = np.where(is_not_pledged, 
                             np.where(is_not_volatile, np.minimum(insured_fraction, deposit_plus_interest), 0), 
                             np.where(is_not_volatile, np.minimum(insured_fraction, df1.loc[is_short_term.values, 'Interest Payable']), 0))
    
    # Create a new DataFrame for storing result
    result_df = pd.DataFrame()
    result_df['Customer ID'] = df1['Customer ID']
    result_df['Stable Amount (Principal + Interest)'] = stable_amount
    
    # Replace NaNs and infinities with zeros
    result_df['Stable Amount (Principal + Interest)'] = result_df['Stable Amount (Principal + Interest)'].replace([np.nan, np.inf, -np.inf], 0)
    
    # Add result to output DataFrame
    output_df['Stable Amount (Principal + Interest)'] = result_df['Stable Amount (Principal + Interest)']

    

    #Unstable Amount
    # Tính giá trị trong IF
    value_if = df1['Deposit balance'] + np.where(output_df['Days till next interet payment'] == '30 or Less', df1['Interest Payable'], 0) - output_df['Stable Amount (Principal + Interest)']
    value_else = np.where(output_df['Days till next interet payment'] == '30 or Less', df1['Interest Payable'], 0) - output_df['Stable Amount (Principal + Interest)']
    
    # Áp dụng công thức chính
    output_df['Unstable Amount (Principal + Interest)'] = np.where(output_df['Exclusion Flag for Pledged to Loans'] == 'No',
                                                                  value_if,
                                                                  value_else
                                                                 )
    output_df['Unstable Amount (Principal + Interest)'] = output_df['Unstable Amount (Principal + Interest)'].clip(lower=0)
    #Unstable Run-Off Factor
    output_df['Concat'] = output_df['Retail/Wholesale'] + output_df['Product type']
    merged_df = output_df.merge(df9[["Concat", "Run-Off Factor"]], left_on="Concat", right_on="Concat", how="left")
    output_df["Unstable Run-Off Factor"] = merged_df["Run-Off Factor"]
    output_df['Unstable Run-Off Factor'] = output_df['Unstable Run-Off Factor'].str.rstrip('%').astype('float') / 100.0
    
    #Stable Run-off Factor
    output_df['Stable Run-off Factor'] = 0.05
    
    #Stable Run-Off Amount
    output_df['Stable Run-Off Amount'] = np.where(
        (output_df['Days To Maturity'] == 'More Than 30 Days') & ((df1['Legal Right to Withdraw?'] == 'No') | (df1['Significant Penalty Flag'] == 'Yes')),
        0,
        output_df['Stable Amount (Principal + Interest)'] * output_df['Stable Run-off Factor']
    )
    
    #Unstable Run-off amount
    output_df['Unstable Run-Off Amount'] = np.where(
        (output_df['Days To Maturity'] == 'More Than 30 Days') & ((df1['Legal Right to Withdraw?'] == 'No') | (df1['Significant Penalty Flag'] == 'Yes')),
        0,
        output_df['Unstable Amount (Principal + Interest)'] * output_df['Unstable Run-Off Factor']
    )
    
    # Total Weighted Cash Outflow 
    output_df['Total Weighted Cash Outflow'] = output_df['Stable Run-Off Amount'] + output_df['Unstable Run-Off Amount']
    output_df = output_df.drop('Concat', axis=1)
    final_output_df = df1.join(output_df)
    
    
    return final_output_df
