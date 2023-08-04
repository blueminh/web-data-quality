class FetchDataService {
    getLcrQuickDashBoard() {
        const lcrData =  {
            title: "Liquidity Coverage Ratio - Quick Dashboard",
            numberOfRows: 4,
            numberOfCols: 2,
            rows: [
                {
                    rowTitle: {
                        title: "Total HQLA",
                        subTitle: "Tổng tài sản thanh khoản có chất lượng cao"
                    },
                    data: [
                        0
                    ]
                },
                {
                    rowTitle: {
                        title: "Total net cash outflows",
                        subTitle: "Tổng dòng tiền ra ròng"
                    },
                    data: [
                        0
                    ]
                },
                {
                    rowTitle: {
                        title: "LCR minimum requirements",
                        subTitle: "Yêu cầu tỷ lệ LCR tối thiểu"
                    },
                    data: [
                        "100%"
                    ]
                },
                {
                    rowTitle: {
                        title: "Liquidity Coverage Ratio",
                        subTitle: "Tỷ lệ bao phủ thanh khoản"
                    },
                    data: [
                        "0%"
                    ]
                },
                {
                    rowTitle: {
                        title: "Remark",
                        subTitle: "Nhận xét"
                    },
                    data: [
                        "Below minimum requirements / Chưa đặt yêu cầu tối thiểu"
                    ]
                },
            ]
        }
        return lcrData
    }

    getNsfrQuickDashBoard() {
        return {
            title: "Net Stable Funding Ratio Ratio - Quick Dashboard",
            numberOfRows: 4,
            numberOfCols: 2,
            rows: [
                {
                    rowTitle: {
                        title: "Available Stable Funding",
                        subTitle: "Nguồn vốn ổn định sẵn có"
                    },
                    data: [
                        "120,062,649,450,300"
                    ]
                },
                {
                    rowTitle: {
                        title: "Required Stable Funding",
                        subTitle: "Nguồn vốn ổn định yêu cầu"
                    },
                    data: [
                        "65,664,197,224,010"
                    ]
                },
                {
                    rowTitle: {
                        title: "NSFR Minimum requirement",
                        subTitle: "Yêu cầu tỷ lệ NSFR tối thiểu"
                    },
                    data: [
                        "100%"
                    ]
                },
                {
                    rowTitle: {
                        title: "Net Stable Funding Ratio",
                        subTitle: "Tỷ lệ nguồn vốn ổn định ròng"
                    },
                    data: [
                        "183%"
                    ]
                },
                {
                    rowTitle: {
                        title: "Remark",
                        subTitle: "Nhận xét"
                    },
                    data: [
                        "Meet minimum requirement / Tuân thủ theo yêu cầu tối thiểu"
                    ]
                },
            ]
        }
    }
}

const service = new FetchDataService()

export default service