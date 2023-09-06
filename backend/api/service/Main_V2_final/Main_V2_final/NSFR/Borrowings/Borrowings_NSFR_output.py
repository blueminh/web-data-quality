"""
@Author: Minh Anh
@Status: Completed
"""

import os
import pandas as pd
import numpy as np
from ..Borrowings import Borrowings_output
from ...Input_Files import getFiles

from datetime import datetime

def parse_date(date_str):
    if not date_str:  # Check for empty strings
        default_date = datetime(2000, 1, 1)
        return default_date
    elif date_str == "0":
        default_date = datetime(2000, 1, 1)
        return default_date
    else:
        try:
            parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
            return parsed_date
        except ValueError:
            return None


def nsfr_borrowings(input_date_str):
    input_folder_path = "Borrowings"
    df1 = getFiles.getFileByName(input_folder_path, f'Borrowings_{input_date_str}.csv')
    df2 =  Borrowings_output.lcr_borrowing(input_date_str)
    df3 = getFiles.getFileByName(input_folder_path, 'Borrowings Mapping.csv')

    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()

    output_df['Principal payment Less than 6 months'] = df2['Counterparty Category'].map(df3.set_index('Counterparty Type')['Less than 6 months']) 
    output_df['Principal payment 6 months to 1 year'] = df2['Counterparty Category'].map(df3.set_index('Counterparty Type')['6 months to 1 year']) 
    output_df['Principal payment More than 1 year'] = df2['Counterparty Category'].map(df3.set_index('Counterparty Type')['More than 1 year']) 

    df1['Principal Amount Less than 6 months'] = df1['Principal Amount Less than 6 months'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['Principal Amount 6 months to 1 year'] = df1['Principal Amount 6 months to 1 year'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['Principal Amount More than 1 year'] = df1['Principal Amount More than 1 year'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['Principal payment Less than 6 months'] = output_df['Principal payment Less than 6 months'].str.rstrip('%').astype(float) /100
    output_df['Principal payment 6 months to 1 year'] = output_df['Principal payment 6 months to 1 year'].str.rstrip('%').astype(float)/100
    output_df['Principal payment More than 1 year'] = output_df['Principal payment More than 1 year'].str.rstrip('%').astype(float)/100
    
    output_df['Total Principal ASF Amount'] = (df1[['Principal Amount Less than 6 months', 'Principal Amount 6 months to 1 year', 'Principal Amount More than 1 year']].values * output_df[['Principal payment Less than 6 months', 'Principal payment 6 months to 1 year', 'Principal payment More than 1 year']].values).sum(axis=1)

    df1['Next interest payment due date'] = df1['Next interest payment due date'].apply(parse_date)
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'])

    difference = (df1['Next interest payment due date'] - df2['Reporting Date']).dt.days

    conditions = [
        difference >= 360,
        (difference < 360) & (difference >= 180),
        difference < 180
    ]

    choices = [
        "More than 1 year",
        "6 months to 1 year",
        "Less than 6 months"
    ]

    output_df["Remaining Maturity for Accrued Interest"] = np.select(conditions, choices, default=np.nan)

    conditions = [
        output_df["Remaining Maturity for Accrued Interest"] == "Less than 6 months",
        output_df["Remaining Maturity for Accrued Interest"] == "6 months to 1 year",
        output_df["Remaining Maturity for Accrued Interest"] == "More than 1 year"
    ]

    choices = [
        0.0,
        0.5,
        1.0
    ]

    output_df["ASF factor for Accrued Interest"] = np.select(conditions, choices, default=np.nan)
        
    output_df['Total Principal ASF Amount'] = output_df['Total Principal ASF Amount'].astype(float)
    df1['Accrued Interest'] = df1['Accrued Interest'].str.replace(',', '').replace(' -   ', '0').astype(float)
    output_df['Total Interest ASF Amount'] = output_df["ASF factor for Accrued Interest"] * df1['Accrued Interest']

    output_df['Total ASF Amount'] = output_df['Total Interest ASF Amount'] + output_df['Total Principal ASF Amount']

    # Concatenate df1 and output_df along the column axis.
    final_output_df = df2.join(output_df)
    final_output_df['Accrued Interest'] = final_output_df['Accrued Interest'].str.replace(',', '').astype(float)
    final_output_df['Principal Amount Less than 6 months'] = final_output_df['Principal Amount Less than 6 months'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df['Principal Amount 6 months to 1 year'] = final_output_df['Principal Amount 6 months to 1 year'].str.replace(',', '').replace(' -   ', '0').astype(float)
    final_output_df['Principal Amount More than 1 year'] = final_output_df['Principal Amount More than 1 year'].str.replace(',', '').replace(' -   ', '0').astype(float)
  
    return final_output_df