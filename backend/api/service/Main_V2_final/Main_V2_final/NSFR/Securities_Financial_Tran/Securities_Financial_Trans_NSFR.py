import os
import pandas as pd
import numpy as np
from .Securities_Financial_Trans import Securities_Financial_Trans

def nsfr_securitiesfinancialtrans():
    path = os.path.dirname(os.path.realpath(__file__))
    df1 =  pd.read_csv(os.path.join(path, 'Securities_Financial_Trans', 'input', 'Securities Financial Trans.csv'))
    df2 = Securities_Financial_Trans.lcr_securitiesfinancialtrans(os.path.join(path, 'Securities_Financial_Trans'))
    df3 =  pd.read_csv(os.path.join(path, 'Securities_Financial_Trans', 'input', 'SFT MAPPING.csv'))
    df4 =  pd.read_csv(os.path.join(path, 'Securities_Financial_Trans', 'input', 'Borrowings Mapping.csv'))

    df1.fillna(0, inplace=True)
    #output dataframe
    output_df = pd.DataFrame()


    #Days To Maturity
    df1['Maturity Date'] = pd.to_datetime(df1['Maturity Date'], errors='coerce')
    df1['Next Interest Payment Due Date'] = pd.to_datetime(df1['Next Interest Payment Due Date'], errors='coerce')
    df2['Reporting Date'] = pd.to_datetime(df2['Reporting Date'], errors='coerce')

    days_to_maturity = (df1['Maturity Date'] - df2['Reporting Date']).dt.days
    conditions = [
        days_to_maturity > 360,
        (days_to_maturity <= 360) & (days_to_maturity > 180),
        days_to_maturity <= 180
    ]
    choices = [
        "More than 1 year",
        "6 months to 1 year",
        "Less than 6 months"
    ]
    output_df["Days To Maturity"] = np.select(conditions, choices)

    #Remaining Maturity for Accrued Interest
    remaining_maturity_for_accrued_interest = (df1['Next Interest Payment Due Date'] - df2['Reporting Date']).dt.days
    conditions = [
        remaining_maturity_for_accrued_interest > 360,
        (remaining_maturity_for_accrued_interest <= 360) & (remaining_maturity_for_accrued_interest > 180),
        remaining_maturity_for_accrued_interest <= 180
    ]
    choices = [
        "More than 1 year",
        "6 months to 1 year",
        "Less than 6 months"
    ]
    output_df["Remaining Maturity for Accrued Interest"] = np.select(conditions, choices)

    #Collateral Asset level
    output_df['Collateral Asset level'] = df2['HQLA Asset']

    #Risk Weight
    df1['Underlying Asset Issuer C41 Risk Weight'] = df1['Underlying Asset Issuer C41 Risk Weight'].astype(str).str.rstrip('%').astype('float') / 100.0
    conditions = [
        df1['Underlying Asset Issuer C41 Risk Weight'] > 0.35,
        df1['Underlying Asset Issuer C41 Risk Weight'] <= 0.35
    ]
    choices = [
        "35% or higher",
        "35% or lower"
    ]
    output_df["Risk Weight"] = np.select(conditions, choices)

    #RSF Factor
    output_df['lookup_key'] = df2['Counterparty Category'].astype(str) + output_df['Days To Maturity'].astype(str) + output_df['Collateral Asset level'].astype(str) + output_df['Risk Weight'].astype(str)
    df3['lookup_key'] = df3['Concat']
    output_df = output_df.merge(df3[['lookup_key', 'RSF Factor']], how='left', on='lookup_key')
    output_df = output_df.rename(columns={'RSF Factor': 'RSF Factor'})
    output_df = output_df.drop(columns=['lookup_key'])

    #RSF Factor for Accrued Interest
    output_df['RSF Factor for Accrued Interest'] = 1
    output_df['RSF Factor for Accrued Interest'] = output_df['RSF Factor for Accrued Interest'].astype(float)
    #Total RSF Amount
    df1['Book Value'] = df1['Book Value'].str.replace(',', '').astype(float)
    df1['Provision'] = df1['Provision'].str.replace(',', '').replace(' -   ', '0').astype(float)
    df1['Accrued Interest'] = df1['Accrued Interest'].str.replace(',', '').astype(float)
    output_df['RSF Factor'] = output_df['RSF Factor'].str.rstrip('%').astype('float') / 100.0
    calculation = output_df['RSF Factor'] * (df1['Book Value'] - df1['Provision']) + df1['Accrued Interest'] * output_df['RSF Factor for Accrued Interest']

    output_df['Total RSF Amount'] = np.where(
        df2['Transaction Type'] == 'Secured Lending',
        calculation,
        0)

    #ASF Factor
    conditions = [
        (output_df['Days To Maturity'] == "Less than 6 months"),
        (output_df['Days To Maturity'] == "6 months to 1 year"),
        (output_df['Days To Maturity'] == "More than 1 year"),
    ]
    choices = [0, 0.5, 1]
    output_df['ASF Factor'] = np.select(conditions, choices, default=0)

    #Principal payment 6 months
    output_df['Principal payment Less than 6 months'] = df2['Counterparty Category'].map(df4.set_index('Counterparty Type')['Less than 6 months'])
    output_df['Principal payment 6 months to 1 year'] = df2['Counterparty Category'].map(df4.set_index('Counterparty Type')['6 months to 1 year'])
    output_df['Principal payment More than 1 year'] = df2['Counterparty Category'].map(df4.set_index('Counterparty Type')['More than 1 year'])
    df1['Next Principal Payment Amount'] = df1['Next Principal Payment Amount'].str.replace(",","").astype(float)
    #ASF Factor for Accrued Interest
    conditions = [
        (output_df['Remaining Maturity for Accrued Interest'] == 'Less than 6 months'),
        (output_df['Remaining Maturity for Accrued Interest'] == '6 months to 1 year'),
        (output_df['Remaining Maturity for Accrued Interest'] == 'More than 1 year')
    ]

    choices = [0.0, 0.5, 1.0]
    output_df['ASF Factor for Accrued Interest'] = np.select(conditions, choices, default=np.nan)
    df1['Principal Amount Less than 6 months'] = df1['Principal Amount Less than 6 months'].str.replace(',', '').replace(' -   ', '0').astype('float')
    df1['Principal Amount 6 months to 1 year'] = df1['Principal Amount 6 months to 1 year'].str.replace(',', '').replace(' -   ', '0').astype('float')
    df1['Principal Amount More than 1 year'] = df1['Principal Amount More than 1 year'].str.replace(',', '').replace(' -   ', '0').astype('float')
    output_df['Principal payment Less than 6 months'] = output_df['Principal payment Less than 6 months'].str.rstrip('%').astype('float') / 100.0
    output_df['Principal payment 6 months to 1 year'] = output_df['Principal payment 6 months to 1 year'].str.rstrip('%').astype('float') / 100.0
    output_df['Principal payment More than 1 year'] = output_df['Principal payment More than 1 year'].str.rstrip('%').astype('float') / 100.0
    #Total ASF Amount
    # Create the conditions
    conditions = [
        (df2['Transaction type'] == 'Secured Borrowing') & (df1['Transaction Category'] == 'Borrowings'),
        (df2['Transaction type'] == 'Secured Borrowing') & (df1['Transaction Category'] != 'Borrowings'),
    ]

    # Create the choices
    choices = [
        np.sum(df1[['Principal Amount Less than 6 months', 'Principal Amount 6 months to 1 year', 'Principal Amount More than 1 year']].values * output_df[['Principal payment Less than 6 months', 'Principal payment 6 months to 1 year', 'Principal payment More than 1 year']].values, axis=1) + output_df['ASF Factor for Accrued Interest'] * df1['Book Value'],
        output_df['ASF Factor'] * df1['Next Principal Payment Amount'] + df1['Accrued Interest'] * output_df['ASF Factor for Accrued Interest'],
    ]

    # Apply the conditions and choices to the DataFrame
    output_df['Total ASF Amount'] = np.select(conditions, choices, default=0)

    final_output_df = df2.join(output_df)
    final_output_df = final_output_df.drop('Concat', axis=1)
    final_output_df['Book Value'] = final_output_df['Book Value'].str.replace(',', '').astype(float)
    final_output_df['Principal Amount Less than 6 months'] = final_output_df['Principal Amount Less than 6 months'].str.replace(',', '').replace(' -   ', '0').astype('float')
    final_output_df['Principal Amount 6 months to 1 year'] = final_output_df['Principal Amount 6 months to 1 year'].str.replace(',', '').replace(' -   ', '0').astype('float')
    final_output_df['Principal Amount More than 1 year'] = final_output_df['Principal Amount More than 1 year'].str.replace(',', '').replace(' -   ', '0').astype('float')
    final_output_df['Underlying Asset Issuer C41 Risk Weight'] = final_output_df['Underlying Asset Issuer C41 Risk Weight'].str.rstrip('%').astype('float') / 100.0
    final_output_df = final_output_df.iloc[:16]
    return final_output_df

