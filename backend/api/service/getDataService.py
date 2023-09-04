from .Main_V2_final.Main_V2_final.LCR.main_LCR import main as main_lcr
import math
from datetime import datetime


def get_dashboard_lcr_nsfr_data(date):
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
                "data": [0]
            },
            {
                "rowTitle": {
                    "title": "Total net cash outflows",
                    "subTitle": "Tổng dòng tiền ra ròng"
                },
                "data": [0]
            },
            {
                "rowTitle": {
                    "title": "LCR minimum requirements",
                    "subTitle": "Yêu cầu tỷ lệ LCR tối thiểu"
                },
                "data": ["100%"]
            },
            {
                "rowTitle": {
                    "title": "Liquidity Coverage Ratio",
                    "subTitle": "Tỷ lệ bao phủ thanh khoản"
                },
                "data": ["0%"]
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data": ["Below minimum requirements / Chưa đặt yêu cầu tối thiểu"]
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
                "data": [
                    "120,062,649,450,300"
                ]
            },
            {
                "rowTitle": {
                    "title": "Required Stable Funding",
                    "subTitle": "Nguồn vốn ổn định yêu cầu"
                },
                "data": [
                    "65,664,197,224,010"
                ]
            },
            {
                "rowTitle": {
                    "title": "NSFR Minimum requirement",
                    "subTitle": "Yêu cầu tỷ lệ NSFR tối thiểu"
                },
                "data": [
                    "100%"
                ]
            },
            {
                "rowTitle": {
                    "title": "Net Stable Funding Ratio",
                    "subTitle": "Tỷ lệ nguồn vốn ổn định ròng"
                },
                "data": [
                    "183%"
                ]
            },
            {
                "rowTitle": {
                    "title": "Remark",
                    "subTitle": "Nhận xét"
                },
                "data": [
                    "Meet minimum requirement / Tuân thủ theo yêu cầu tối thiểu"
                ]
            },
        ]
    }

    return {"lcr_data": lcr_data, "nsfr_data": nsfr_data}

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
    def __init__(self, code, depth, data, children=[]):
        self.code = code # need code to fetch data
        self.depth = depth # depth for displaying collapesable componenets
        self.data = data # array of data, including the index
        self.children = children # children
        self.hasChildren = len(children) > 0


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
            "hasChildren":self.hasChildren
        }

def get_lcr_data(date):
    # all python script use the format day-month-year
    date_object = datetime.strptime(date, '%Y-%m-%d')
    # Format the date as '28-08-2023'
    formatted_date = date_object.strftime('%d-%m-%Y')

    df = main_lcr(formatted_date)
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