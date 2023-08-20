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