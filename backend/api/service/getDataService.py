from .Main_V2_final.Main_V2_final.LCR.main_LCR import main as main_lcr
from .Main_V2_final.Main_V2_final.main_Home import main as main_home
from .Main_V2_final.Main_V2_final.NSFR.main_NSFR import main as main_nsfr
import math
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

from ..models import CalculatedData

class Row:
    def __init__(self, code, depth, data, children=[], volatility_data = {
        "x":[2020, 2021,2022],
        "y":[29, 34, 16]
    }):
        self.code = code # need code to fetch data
        self.depth = depth # depth for displaying collapesable componenets
        self.data = data # array of data, including the index
        self.children = children # children
        self.hasChildren = len(children) > 0
        self.volatility_data = volatility_data


    def setChildren(self, children):
        self.hasChildren = len(children) > 0
        self.children = children

    def toJSON(self):
        def convert_nan(value):
            if isinstance(value, float) and math.isnan(value):
                return "0"
            return value
        
        json_children = [child.toJSON() for child in self.children]
        converted_data = [convert_nan(value) for value in self.data]

        return {
            "code":self.code,
            "depth":self.depth,
            "data":converted_data,
            "children":json_children,
            "hasChildren":self.hasChildren,
            "volatility_data":self.volatility_data
        }
    
"""
    Helper function to replace all NaN values with the empty string
"""
def replace_nan_with_empty_string(data):
    for row in data['rows']:
        if pd.isna(row['data']):
            row['data'] = ''
        # for value in row['data']:
        #     if pd.isna(value):
        #         row['data'] = ''


"""
    Helper function to persist data in the database
    :params
        row: a Row object 
        date: the date to save the data
        index_of_important_stat: a row typically consists of multiple data points. Only 1 point is persisted
"""
def save_data(row, date, index_of_important_stat):
    result_string = row.get("data")[index_of_important_stat]
    new_calculated_data = CalculatedData(field_name=row.get("code"), date=date, value=result_string)
    new_calculated_data.save()
    for child in row.get("children"):
        save_data(child, date, index_of_important_stat)


"""
    Convert the LCR df into a json object that contains Row objects.
    Each row has the code for the index

    :return: an array containing multiple Row objects. Note that Row is a recursive structure
"""
def convert_lcr_df_to_json(df):
    hqla = Row("hqla", 0, ["", "High-quality liquid assets", "Tài sản thanh khoản có chất lượng cao", "", ""])
    hqla.setChildren(
        [
            Row("total_1_assets", 2, df.iloc[0].tolist()),
            Row("total_2a_assets", 2, df.iloc[1].tolist()),
            Row("total_2b_assets", 2, df.iloc[2].tolist()),
            Row("adj_40_of_2a", 2, df.iloc[3].tolist()),
            Row("adj_15_of_2b", 2, df.iloc[4].tolist()),
            Row("total_hqla", 1, df.iloc[5].tolist()),
        ]
    )

    cash_outflow = Row("cash_outflows", 0, ["", "Cash outflows", "Các dòng tiền ra", "", ""])
    cash_outflow.setChildren(
        [
            Row('retail_dep', 2, df.iloc[7].tolist(), [
                Row('stale_dep', 3, df.iloc[8].tolist()),
                Row('less_stale_dep', 3, df.iloc[9].tolist())
            ]),
            Row('unsec_wholesale_fund', 2, df.iloc[10].tolist(), [
                Row('opt_dep', 3, df.iloc[11].tolist()),
                Row('non_opt_dep', 3, df.iloc[12].tolist()),
                Row('unsec_debt', 3, df.iloc[13].tolist()),
            ]),
            Row('sec_wholesale_fund', 2, df.iloc[14].tolist()),
            Row('add_req', 2, df.iloc[15].tolist(), [
                Row('deri_expo', 3, df.iloc[16].tolist()),
                Row('loss_of_fund', 3, df.iloc[17].tolist()),
                Row('credit', 3, df.iloc[18].tolist()),
            ]),
            Row('other_contrac', 2, df.iloc[19].tolist()),
            Row('other_contingent', 2, df.iloc[20].tolist()),
            Row('total_outflows', 1, df.iloc[21].tolist())
        ]
    )

    cash_inflow = Row("cash_inflows", 0, ["", "Cash inflows", "Các dòng tiền vào", "", ""])
    cash_inflow.setChildren(
        [
            Row('sec_lend', 2, df.iloc[23].tolist()),
            Row('inflows_from_fully', 2, df.iloc[24].tolist()),
            Row('other_inflows', 2, df.iloc[25].tolist()),
            Row('total_inflows', 1, df.iloc[26].tolist())
        ]
    )

    total_hqla = Row('total_hqla', 1, df.iloc[28].tolist())
    total_net_outflow = Row('total_net_outflow', 1, df.iloc[29].tolist())
    liquid_cov_ratio = Row('liquid_cov_ratio', 1, df.iloc[30].tolist())

    lcr_data = [hqla.toJSON(), cash_outflow.toJSON(), cash_inflow.toJSON(), total_hqla.toJSON(), total_net_outflow.toJSON(), liquid_cov_ratio.toJSON()]
    return lcr_data


"""
    Persist the data into the database

    :params:
        lcr_json_data: an array containing multiple Row objects
        reporting_date: the date of the data
"""
def save_lcr_data(lcr_json_data, reporting_date):
    lcr_data_string = json.dumps(lcr_json_data)
    new_calculated_data = CalculatedData(field_name="lcr", date=reporting_date, value=lcr_data_string)
    new_calculated_data.save()

    for item in lcr_json_data:
        save_data(item, date=reporting_date, index_of_important_stat=4)


"""
    Calculate the LCR board and persist LCR data into the database
    
    :params:
        request_data: is an json object that contains these information:
            - reportingDate: the chosen reporting date by the users. This is used for finding the
            corresponding tables (note that data tables' names are in the format "tablename_date")
            - extraTables: any tables that are NOT on reportingDate are specified here with the 
            actual date to be used. For example: 
                extraTables: {
                    "Borrowings": 28-08-2023,
                    "Derivatives": 30-08-2023
                }
    
    :return: an array containing multiple Row objects containing LCR data
"""
def calculate_lcr(request_data):
    df = main_lcr(request_data)
    lcr_json_data = convert_lcr_df_to_json(df)
    save_lcr_data(lcr_json_data, request_data.get("reportingDate"))
    return lcr_json_data


"""
    Convert the NSFR df into a json object that contains Row objects.
    Each row has the code for the index

    :return: an array containing multiple Row objects. Note that Row is a recursive structure
"""
def convert_nsfr_df_to_json(df):
    capital = Row("capital", 2, df.iloc[0].tolist())
    capital.setChildren(
        [
            Row("reg_cap", 3, df.iloc[1].tolist()),
            Row("other_cap_instru", 3, df.iloc[2].tolist()),
        ]
    )

    retail_dep_and_dep_small_business = Row("retail_dep_and_dep_small_business", 2, df.iloc[3].tolist())
    retail_dep_and_dep_small_business.setChildren(
        [
            Row("stable_dep", 3, df.iloc[4].tolist()), 
            Row("less_stable_dep", 3, df.iloc[5].tolist()),
        ]
    )

    wholesale_func = Row("wholesale_func", 2, df.iloc[6].tolist())
    wholesale_func.setChildren(
        [
            Row("op_dep", 3, df.iloc[7].tolist()),
            Row("other_wholesale_func", 3, df.iloc[8].tolist()),
        ]
    )

    liability_with_assets  = Row("liability_with_assets", 2, df.iloc[9].tolist())

    other_liability  = Row("other_liability", 2, df.iloc[10].tolist())
    other_liability.setChildren(
        [
            Row("nsfr_derivative", 3, df.iloc[11].tolist()),
            Row("all_other", 3, df.iloc[12].tolist()),
        ]
    )

    total_asf  = Row("total_asf", 2, df.iloc[13].tolist())
    require_stable_fund = Row("require_stable_fund", 0, ["", "Required Stable Funding (RSF)", "", "", "", "","",""])

    total_nsfr_hqla  = Row("total_nsfr_hqla", 2, df.iloc[15].tolist())
    dep_at_others  = Row("dep_at_others", 2, df.iloc[16].tolist())
    perform_loan_and_sec  = Row("perform_loan_and_sec", 2, df.iloc[17].tolist())
    perform_loan_and_sec.setChildren(
        [
            Row("perform_to_fin_ins_1", 3, df.iloc[18].tolist()),
            Row("pergom_to_fin_ins_2", 3, df.iloc[19].tolist()),
            Row("pergom_to_non_fin_1", 3, df.iloc[20].tolist()),
            Row("pergom_to_non_fin_2", 3, df.iloc[21].tolist()),
            Row("pergom_to_rw>", 3, df.iloc[22].tolist()),
            Row("pergom_to_rw<", 3, df.iloc[23].tolist()),
            Row("sec_not_in_def", 3, df.iloc[24].tolist())
        ]
    )


    assets_with_liabilities  = Row("assets_with_liabilities", 2, df.iloc[25].tolist())

    other_assets  = Row("other_assets", 2, df.iloc[26].tolist())
    other_assets.setChildren([
        Row("physical_trade", 3, df.iloc[27].tolist()),
        Row("initial_margin", 3, df.iloc[28].tolist()),
        Row("nsfr_derivatives", 3, df.iloc[29].tolist()),
        Row("nsfr_derivatives_2", 3, df.iloc[30].tolist()),
        Row("all_other_assets", 3, df.iloc[31].tolist())
    ])

    obs  = Row("obs", 2, df.iloc[32].tolist())

    total_rsf  = Row("total_rsf", 2, df.iloc[33].tolist())

    nsfr  = Row("nsfr", 0, df.iloc[34].tolist())

    require_stable_fund.setChildren([
        total_nsfr_hqla,
        dep_at_others,
        perform_loan_and_sec, 
        assets_with_liabilities, 
        other_assets,
        obs, 
        total_rsf
    ])

    nsfr_data = [
        capital.toJSON(), 
        retail_dep_and_dep_small_business.toJSON(),
        wholesale_func.toJSON(), 
        liability_with_assets.toJSON(), 
        other_liability.toJSON(), 
        total_asf.toJSON(), 
        require_stable_fund.toJSON(), 
        nsfr.toJSON()
    ]
    return nsfr_data


"""
    Helper function to persist data in the database
    :params
        row: a Row object 
        date: the date to save the data
        index_of_important_stat: a row typically consists of multiple data points. Only 1 point is persisted
"""
def save_nsfr_data(nsfr_json_data, reporting_date):
    nsfr_data_string = json.dumps(nsfr_json_data)
    new_calculated_data = CalculatedData(field_name="nsfr", date=reporting_date, value=nsfr_data_string)
    new_calculated_data.save()

    for item in nsfr_json_data:
        save_data(item, date=reporting_date, index_of_important_stat=7)


"""
    Calculate the NSFR board and persist NSFR data into the database
    
    :params:
        request_data: is an json object that contains these information:
            - reportingDate: the chosen reporting date by the users. This is used for finding the
            corresponding tables (note that data tables' names are in the format "tablename_date")
            - extraTables: any tables that are NOT on reportingDate are specified here with the 
            actual date to be used. For example: 
                extraTables: {
                    "Borrowings": 28-08-2023,
                    "Derivatives": 30-08-2023
                }
    
    :return: an array containing multiple Row objects containing NSFR data
"""
def calculate_nsfr(request_data):
    df = main_nsfr(request_data)
    nsfr_json_data = convert_nsfr_df_to_json(df)
    save_nsfr_data(nsfr_json_data, request_data.get("reportingDate"))
    return nsfr_json_data


"""
    Calculate the both NSFR and LCR boards and persist them into the database
    
    :params:
        request_data: is an json object that contains these information:
            - reportingDate: the chosen reporting date by the users. This is used for finding the
            corresponding tables (note that data tables' names are in the format "tablename_date")
            - extraTables: any tables that are NOT on reportingDate are specified here with the 
            actual date to be used. For example: 
                extraTables: {
                    "Borrowings": 28-08-2023,
                    "Derivatives": 30-08-2023
                }
"""
def get_dashboard_lcr_nsfr_data(request_data):
    lcr_df = main_lcr(request_data)
    lcr_json_data = convert_lcr_df_to_json(lcr_df)
    save_lcr_data(lcr_json_data, request_data.get("reportingDate"))
    nsfr_df = main_nsfr(request_data)
    nsfr_json_data = convert_nsfr_df_to_json(nsfr_df)
    save_nsfr_data(nsfr_json_data, request_data.get("reportingDate"))
    
    lcr_data = {
        "title": "Liquidity Coverage Ratio - Quick Dashboard",
        "numberOfRows": 4,
        "numberOfCols": 2,
        "rows": [
            {
                "rowTitle": {
                    "title": "Total HQLA",
                    "subTitle": "Tổng tài sản thanh khoản có chất lượng cao"
                },
                "data": lcr_df.loc[28, 'Blank 2'] if lcr_df.loc[28, 'Blank 2'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "Total net cash outflows",
                    "subTitle": "Tổng dòng tiền ra ròng"
                },
                "data": lcr_df.loc[29, 'Blank 2'] if lcr_df.loc[29, 'Blank 2'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "LCR minimum requirements",
                    "subTitle": "Yêu cầu tỷ lệ LCR tối thiểu"
                },
                "data": 1.0
            },
            {
                "rowTitle": {
                    "title": "Liquidity Coverage Ratio",
                    "subTitle": "Tỷ lệ bao phủ thanh khoản"
                },
                "data":lcr_df.loc[30, 'Blank 2'] if lcr_df.loc[29, 'Blank 2'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data": "Meet minimum requirement/Tuân thủ yêu cầu tối thiểu" if lcr_df.loc[30, 'Blank 2'] >= 1 else "Below minimum requirement/Chưa đạt yêu cầu tối thiểu"
            },
        ]
    }

    nsfr_data = {
        "title": "Net Stable Funding Ratio Ratio - Quick Dashboard",
        "numberOfRows": 4,
        "numberOfCols": 2,
        "rows": [
            {
                "rowTitle": {
                    "title": "Available Stable Funding",
                    "subTitle": "Nguồn vốn ổn định sẵn có"
                },
                "data": nsfr_df.loc[13, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[13, 'Blank 5'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "Required Stable Funding",
                    "subTitle": "Nguồn vốn ổn định yêu cầu"
                },
                "data": nsfr_df.loc[33, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[33, 'Blank 5'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "NSFR Minimum requirement",
                    "subTitle": "Yêu cầu tỷ lệ NSFR tối thiểu"
                },
                "data": 1.0
            },
            {
                "rowTitle": {
                    "title": "Net Stable Funding Ratio",
                    "subTitle": "Tỷ lệ nguồn vốn ổn định ròng"
                },
                "data": nsfr_df.loc[34, 'Blank 5'] if 'Blank 5' in nsfr_df.columns and nsfr_df.loc[33, 'Blank 5'] is not None else 0
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data":  "Meet minimum requirement/Tuân thủ yêu cầu tối thiểu" if nsfr_df.loc[34, 'Blank 5'] >= 1 else "Below minimum requirement/Chưa đạt yêu cầu tối thiểu"
            },
        ]
    }

    replace_nan_with_empty_string(lcr_data)
    replace_nan_with_empty_string(nsfr_data)

    result = {
        "lcr_data":lcr_data,
        "nsfr_data":nsfr_data
    }
    result_string = json.dumps(result)
    new_calculated_data = CalculatedData(field_name="dashboard_lcr_nsfr", date=request_data.get("reportingDate"), value=result_string)
    new_calculated_data.save()

    return result


"""
    Helper function to find the dates of the last n days
    :params: 
        start_date_str: the date to start counting from
        number_of_days
    
    :return: an array containing the dates of the last n days counting from start_date_str
"""
def get_last_days(start_date_str, number_of_days):
    try:
        # Convert the input date string to a datetime object
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        
        # Create a list to store the result
        date_list = []

        # Generate dates for the last 7 days, including the start date
        for i in range(number_of_days - 1, -1, -1):
            date_list.append((start_date - timedelta(days=i)).strftime("%d-%m-%Y"))

        return date_list
    except ValueError:
            # Handle invalid date format gracefully
            return []
    

"""
    Helper function to find the dates of the last n days, 7 days from each other
    :params: 
        start_date_str: the date to start counting from
        number_of_days
    
    :return: an array containing the dates of the last n days (7 days from each other) counting from start_date_str
    For example call (30-08-2023, 3) would return [16-08-2023, 23-08-2023, 30-08-2023]
"""
def get_last_weeks(start_date_str, number_of_weeks):
    try:
        # Convert the input date string to a datetime object
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        
        # Create a list to store the result
        date_list = []

        # Generate dates for the last 7 days, including the start date
        for i in range(number_of_weeks - 1, -1, -1):
            date_list.append((start_date - timedelta(weeks=i)).strftime("%d-%m-%Y"))

        return date_list
    except ValueError:
            # Handle invalid date format gracefully
            return []
    
"""
    Helper function to find the first dates of the last n months
    :params: 
        start_date_str: the date to start counting from
        number_of_days
    
    :return: an array containing first dates of the last n months counting from start_date_str
    For example call (30-08-2023, 3) would return [01-06-2023, 01-07-2023, 01-08-2023]
"""
def get_first_date_of_last_months(start_date_str, number_of_months):
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        date_list = []
        for i in range(number_of_months - 1, -1, -1):
            date_list.append((start_date - relativedelta(months=i)).replace(day=1).strftime("%d-%m-%Y"))
        
        return date_list
    except ValueError:
            # Handle invalid date format gracefully
            return []
