import { Table, Row, Col} from 'react-bootstrap';
import { useEffect, useState } from "react";
import './homePage.css'
import '../../Global.css'
import FetchDataService from '../../services/fetchDataService'


export default function Homepage() {
    const [lcrData, setLcrData] = useState({
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
    })

    const [nsfrData, setNsfrData] = useState({
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
    })

    // Load data
    useEffect(() => {
        // console.log(FetchDataService.getLcrQuickDashBoard)
        setLcrData(FetchDataService.getLcrQuickDashBoard())
        setNsfrData(FetchDataService.getNsfrQuickDashBoard())
    }, []) 


    function formatDate(date) {
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      
        const dayOfWeek = days[date.getDay()];
        const month = months[date.getMonth()];
        const day = date.getDate();
        const year = date.getFullYear();
      
        return `${dayOfWeek}, ${month} ${day}, ${year}`;
    }
      
    // Get the current date
    const currentDate = new Date();
    
    // Format and display the current date
    const formattedDate = formatDate(currentDate);

    return (
        <div>
            <div id="dashboard-general-info">
                {/* <Row>
                    <Col><p>Select language / Chọn ngôn ngữ</p></Col>
                    <Col>
                    <DropdownButton
                        as={ButtonGroup}
                        key={variant}
                        id={`dropdown-variants-${variant}`}
                        variant={variant.toLowerCase()}
                        title={variant}
                    >
                        <Dropdown.Item eventKey="1">Action</Dropdown.Item>
                        <Dropdown.Item eventKey="2">Another action</Dropdown.Item>
                    </Col>
                </Row> */}
                <Row style={{fontWeight:'bold', fontSize:'larger'}}>
                    <Col>CAO</Col>
                    <Col>{formattedDate}</Col>
                </Row>
            </div>
            <div className='tables-grid'>
                <Row>
                    <Col>
                        <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>{lcrData.title}</td>
                                </tr>
                                {lcrData.rows.map(row => 
                                    <tr>
                                        <td>
                                            <span className='row-title'>{row.rowTitle.title}</span>
                                            <br></br>
                                            <span><em>{row.rowTitle.subTitle}</em></span>
                                        </td>
                                        {row.data.map(rowData =>
                                            <td style={{textAlign: "center"}}>{rowData}</td>
                                        )}
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    </Col>
                    <Col>
                    <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>{nsfrData.title}</td>
                                </tr>
                                {nsfrData.rows.map(row => 
                                    <tr>
                                        <td>
                                            <span className='row-title'>{row.rowTitle.title}</span>
                                            <br></br>
                                            <span><em>{row.rowTitle.subTitle}</em></span>
                                        </td>
                                        {row.data.map(rowData =>
                                            <td style={{textAlign: "center"}}>{rowData}</td>
                                        )}
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    </Col>
                </Row>
            </div>    
        </div>
    )
}