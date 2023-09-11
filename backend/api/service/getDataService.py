from .Main_V2_final.Main_V2_final.LCR.main_LCR import main as main_lcr
from .Main_V2_final.Main_V2_final.main_Home import main as main_home
from .Main_V2_final.Main_V2_final.NSFR.main_NSFR import main as main_nsfr
import math
import pandas as pd

def replace_nan_with_empty_string(data):
    for row in data['rows']:
        if pd.isna(row['data']):
            row['data'] = ''
        # for value in row['data']:
        #     if pd.isna(value):
        #         row['data'] = ''

def get_dashboard_lcr_nsfr_data(request_data):
    # return {"lcr_data": lcr_data, "nsfr_data": nsfr_data}
    result = main_home(request_data)
    lcr_result = result['lcr']
    nsfr_result = result['nsfr']

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
                "data": lcr_result[0]
            },
            {
                "rowTitle": {
                    "title": "Total net cash outflows",
                    "subTitle": "Tổng dòng tiền ra ròng"
                },
                "data": lcr_result[1]
            },
            {
                "rowTitle": {
                    "title": "LCR minimum requirements",
                    "subTitle": "Yêu cầu tỷ lệ LCR tối thiểu"
                },
                "data": lcr_result[2]
            },
            {
                "rowTitle": {
                    "title": "Liquidity Coverage Ratio",
                    "subTitle": "Tỷ lệ bao phủ thanh khoản"
                },
                "data": lcr_result[3]
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data": lcr_result[4]
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
                "data": nsfr_result[0]
            },
            {
                "rowTitle": {
                    "title": "Required Stable Funding",
                    "subTitle": "Nguồn vốn ổn định yêu cầu"
                },
                "data": nsfr_result[1]
            },
            {
                "rowTitle": {
                    "title": "NSFR Minimum requirement",
                    "subTitle": "Yêu cầu tỷ lệ NSFR tối thiểu"
                },
                "data": nsfr_result[2]
            },
            {
                "rowTitle": {
                    "title": "Net Stable Funding Ratio",
                    "subTitle": "Tỷ lệ nguồn vốn ổn định ròng"
                },
                "data": nsfr_result[3]
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data": nsfr_result[4]
            },
        ]
    }

    replace_nan_with_empty_string(lcr_data)
    replace_nan_with_empty_string(nsfr_data)

    return {
        "lcr_data":lcr_data,
        "nsfr_data":nsfr_data
    }

def get_dashboard_bar_charts_data():
    data = [
        {
            "title": "Biểu đồ biến động các cấu phần của LCR",
            "labels": ['2020', '2021', '2022'],
            "datasets": [
                {
                    "label": 'Cash outflow',
                    "data": [10, 20, 17],
                    "backgroundColor": 'rgba(237,125,48,255)',
                },
                {
                    "label": 'Cash inflow',
                    "data": [6, 13.5, 8],
                    "backgroundColor": 'rgba(67,114,196,255)',
                },
                {
                "label": 'HQLA',
                "data": [5, 8, 6],
                "backgroundColor": 'rgba(165,165,165,255)',
            },
            ]
        }, 
        {
            "title": "Biểu đồ biến động cấu phần Cash outflow",
            "labels": ['2020', '2021', '2022'],
            "datasets": [
            {
                "label": 'Rental & small business deposit',
                "data": [9, 10 , 20],
                "backgroundColor": 'rgba(237,125,48,255)',
            },
            {
                "label": 'Unsecured wholesale funding',
                "data": [29, 34, 16],
                "backgroundColor": 'rgba(67,114,196,255)',
            },
            {
                "label": 'Secured wholesale funding',
                "data": [0, 2, 1],
                "backgroundColor": 'rgba(165,165,165,255)',
            },
            {
                "label": 'Additional requirement',
                "data": [8, 4, 10],
                "backgroundColor": 'rgba(237,125,48,255)',
            },
            {
                "label": 'Other contractual funding',
                "data": [0 ,1 , 4],
                "backgroundColor": 'rgba(67,114,196,255)',
            },
            {
                "label": 'Other contingen funding',
                "data": [5 ,7, 6],
                "backgroundColor": 'rgba(165,165,165,255)',
            },
        ]
        }, 
        {
            "title": "Biển đồ biến động cấu phần Cash inflow",
            "labels": ['2020', '2021', '2022'],
            "datasets": [
                {
                    "label": 'Secured landing',
                    "data": [0, 1, 0],
                    "backgroundColor": 'rgba(237,125,48,255)',
                },
                {
                    "label": 'Inflows from fully performing exposures',
                    "data": [6, 9 , 4],
                    "backgroundColor": 'rgba(67,114,196,255)',
                },
                {
                "label": 'Other cash inflows',
                "data": [3, 3, 8],
                "backgroundColor": 'rgba(165,165,165,255)',
                },
            ]
        }
    ]
    return data

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
                return "Nan"
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

def get_lcr_data(request_data):
    # all python script use the format day-month-year
    # date_object = datetime.strptime(date, '%Y-%m-%d')
    # # Format the date as '28-08-2023'
    # formatted_date = date_object.strftime('%d-%m-%Y')
    df = main_lcr(request_data)
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


def get_nsfr_data(request_data):
    df = main_nsfr(request_data)
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
