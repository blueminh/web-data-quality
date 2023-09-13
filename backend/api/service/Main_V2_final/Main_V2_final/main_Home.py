"""
@Author: Khanh Hung & Minh Anh
@Status: Completed
"""
import os
import pandas as pd
import numpy as np
from .LCR import main_LCR
from .NSFR import main_NSFR

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

def lcr_4(df):
    value = df.loc[30, 'Blank 2'] if df.loc[29, 'Blank 2'] is not None else 0
    # result = df.loc[v_1, colname] /  df.loc[v_2, colname] if df.loc[v_2, colname] != 0 else 0
    return value

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

def nsfr_4(nsfr_df):
    value = nsfr_df.loc[34, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[33, 'Blank 5'] is not None else 0
    # result = df.loc[n_1, colname] /  df.loc[n_2, colname] if df.loc[n_2, colname] != 0 else 0
    return value

def nsfr_5(df, n_3, colname):
    
    if df.loc[n_3, colname] >= 1:  
        result = "Meet minimum requirement/Tuân thủ yêu cầu tối thiểu"
    else:
        result = "Below minimum requirement/Chưa đạt yêu cầu tối thiểu"
        
    return result

def main(request_data):
    lcr_df = main_LCR.main(request_data)
    nsfr_df = main_NSFR.main(request_data)
    left_df = set_LCR()
    right_df = set_NSFR()
    
    return {
        "lcr":[
            lcr_1(lcr_df), 
            lcr_2(lcr_df), 
            1.0, 
            lcr_4(lcr_df), 
            lcr_5(left_df, 3, "Values")
        ],
        "nsfr":[
            nsfr_1(nsfr_df), 
            nsfr_2(nsfr_df), 
            1.0, 
            nsfr_4(nsfr_df), 
            nsfr_5(right_df, 3, "Values")
        ]
    }
    

    
if __name__ == "__main__":
    main()
