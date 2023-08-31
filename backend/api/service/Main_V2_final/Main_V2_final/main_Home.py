"""
@Author: Khanh Hung & Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from LCR import main_LCR
from NSFR import main_NSFR

def set_LCR(): 
    data = {
        'Liquidity Coverage Ratio': [
            'Total HQLA/Tổng tài sản thanh khoản có chất lượng cao',
            'Total net cash outflows/Tổng dòng tiền ra ròng',
            'LCR minimum requirement/Yêu cầu tỷ lệ LCR tối thiểu',
            'Liquidity Coverage Ratio/Tỷ lệ bao phủ thanh khoản',
            'Remark/Nhận xét'
        ]
    }

    df = pd.DataFrame(data)        
    df["Values"] = np.nan



    return df

def set_NSFR():
    # Define the data
    data = {
        'Net Stable Funding Ratio': [
            'Available Stable Funding/Nguồn vốn ổn định sẵn có',
            'Required Stable Funding/Nguồn vốn ổn định yêu cầu',
            'NSFR minimum requirement/Yêu cầu tỷ lệ NSFR tối thiểu',
            'Net Stable Funding Ratio/Tỷ lệ nguồn vốn ổn định ròng',
            'Remark/Nhận xét'
        ]

    }
    df = pd.DataFrame(data)        
    df["Values"] = np.nan



    return df

def lcr_1(df):
    value = df.loc[28, 'Blank 2'] if df.loc[28, 'Blank 2'] is not None else 0
    return value

def lcr_2(df):
    value = df.loc[29, 'Blank 2'] if df.loc[29, 'Blank 2'] is not None else 0
    return value

def lcr_4(df, v_1, v_2, colname):

    result = df.loc[v_1, colname] /  df.loc[v_2, colname] if df.loc[v_2, colname] != 0 else 0
    return result

def lcr_5(df, v_3, colname):
    
    if df.loc[v_3, colname] >= 1: 
        result = "Meet minimum requirement/Tuân thủ yêu cầu tối thiểu"
    else:
        result = "Below minimum requirement/Chưa đạt yêu cầu tối thiểu"
        
    return result

def nsfr_1(nsfr_df):
    value = nsfr_df.loc[13, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[13, 'Blank 5'] is not None else 0
    return value

def nsfr_2(nsfr_df):
    value = nsfr_df.loc[33, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[33, 'Blank 5'] is not None else 0
    return value

def nsfr_4(df, n_1, n_2, colname):
    
    result = df.loc[n_1, colname] /  df.loc[n_2, colname] if df.loc[n_2, colname] != 0 else 0
    return result

def nsfr_5(df, n_3, colname):
    
    if df.loc[n_3, colname] >= 1:  
        result = "Meet minimum requirement/Tuân thủ yêu cầu tối thiểu"
    else:
        result = "Below minimum requirement/Chưa đạt yêu cầu tối thiểu"
        
    return result

def main():
    path = os.path.dirname(os.path.realpath(__file__))

    lcr_df = main_LCR.main("28-08-2023")
    nsfr_df = main_NSFR.main(os.path.join(path, 'NSFR'))
    left_df = set_LCR()
    right_df = set_NSFR()

    left_df.at[0, 'Values'] = lcr_1(lcr_df)
    left_df.at[1, 'Values'] = lcr_2(lcr_df)
    left_df.at[2, 'Values'] = '100%'
    left_df.at[3, 'Values'] = lcr_4(left_df, 0, 1, "Values")
    left_df.at[4, 'Values'] = lcr_5(left_df, 3, "Values")

    right_df.at[0, 'Values'] = nsfr_1(nsfr_df)
    right_df.at[1, 'Values'] = nsfr_2(nsfr_df)
    right_df.at[2, 'Values'] = '100%'
    right_df.at[3, 'Values'] = nsfr_4(right_df, 0, 1, "Values")
    right_df.at[4, 'Values'] = nsfr_5(right_df, 3, "Values")
    final_df = pd.concat([left_df, right_df], axis=1)
    print(final_df)

    return final_df
    

    
if __name__ == "__main__":
    main()
