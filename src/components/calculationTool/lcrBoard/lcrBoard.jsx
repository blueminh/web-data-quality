import { useState } from 'react'
import { Table } from 'react-bootstrap';
import './lcrBoard.css'

export default function LCRDashBoard() {
     // eslint-disable-next-line
    const [reportedDate, setReportedDate] = useState("9/30/2022")
     // eslint-disable-next-line
    const [lcrBoardData, setLcrBoardData] = useState({
        columnNames: ["Items", "Khoản mục", "Total unweighted value"],
        sections: [
            {
                sectionName: "High quality liquid asssets",
                sectionNameVn: "Tài sản thanh khoản có chất lượng cao",
                rows: [
                    ["Total Level 1 Assets", "Tổng tài sản thanh khoản Cấp 1", 0],
                    ["Total Level 2A Assets", "Tổng tài sản thanh khoản Cấp 2A", 0],
                    ["Total Level 2B Assets", "Tổng tài sản thanh khoản Cấp 2B", 0],
                    ["Adjustment for 40% cap of Level 2A Assets", "Giá trị điều chỉnh theo ngưỡng trần 40% đối với tài sản thanh khoản cấp 2A", 0],
                    ["Adjustment for 15% cap of Level 2B Assets", "Giá trị điều chỉnh theo ngưỡng trần 40% đối với tài sản thanh khoản cấp 2B", 0],
                    ["TOTAL HQLA", "Tổng tài sản thanh khoản có chất lượng cao", 0],
                ]
            },
            {
                sectionName: "Cash outflows",
                sectionNameVn: "Các dòng tiền ra",
                rows: [
                    ["Retail deposits and deposits from small business customers, of which:", "Tiền gửi của khách hàng bán lẻ và khách hàng kinh doanh nhỏ", 0],
                    ["Stable deposits", "Tiền gửi ổn định", 0],
                    ["Less stable deposits", "Tiền gửi kém ổn định", 0],
                    ["Unsecured wholesale funding, of which:", "Nguồn vốn huy động từ bán buôn không bảo đẩm, trong đó:", 0],
                    ["Operational deposits (all counterparties) and deposits in networks of cooperative banks", "Tiền gửi hoạt dộng và tiền gửi trong mạng lưới các ngân hàng hợp tác", 0],
                    ["Non-operational deposits (all counterparties)", "Tiền gửi không nhằm mục đích hoạt động", 0],
                    ["Unsecured debt", "Chứng khoán nợ không bảo đảm", 0],
                    ["Secured wholesale funding", "Nguồn bốn huy động từ bán buôn được bảo đảm", 0],
                    ["Additional requirements, of which:", "Các yêu cầu bổ sung, trong đó:", 0],
                    ["Outflows related to derivative exposures and other collateral requirements", "Các dòng tiền ra từ các trạng thái phát sinh và các yêu cầu về TSBĐ khác", 0],
                    ["Outflows related to loss of funding on debt products", "DÒng tiền ra từ mất nguồn vốn huy động từ các công cụ nợ", 0],
                    ["Credit and liquidity facilities", "Các cam kết tín dụng và cam kết thanh khoản", 0],
                    ["Other contractual funding obligations", "Các nghĩa vụ theo hợp đồng khác", 0],
                    ["Other contingent funding obligations", "Các nghĩa vụ tài trợ tiềm ẩn khác", 0],
                    ["TOTAL CASH OUTFLOWS", "Tổng dòng tiền ra", 0],
                ]
            },
            {
                sectionName: "Cash inflows",
                sectionNameVn: "Các dòng tiền vào",
                rows: [
                    ["Secured lending (reverse repos and securities borrowing)", "Các giao dịch ho vay được bảo đảm", 0],
                    ["Inflows from fully performing exposures", "Dòng tiền vào từ các khoản cho vay tốt", 0],
                    ["Other cash inflows", "Các dòng tiền vào khác", 0],
                    ["TOTAL CASH INFLOWS", "Tổng dòng tiền vào", 0],
                ]
            },
            {
                sectionName: "Liquid Coverage Ratio",
                sectionNameVn: "Tỉ lệ đảm bảo khả năng thanh khoản LCR",
                rows: [
                    ["Liquid Coverage Ratio", "Tỉ lệ đảm bảo khả năng thanh khoản LCR", 0]
                ]
            }
        ]
    })

    return (
        <div>
            <div id = "generalInfo">
                <div id = "pageTitle">NAB - Basel III Tỷ lệ bao phủ thanh khoản (LCR) - Công bố thông tin (Public Discloure)</div>
                <div>Reported at / Thởi điểm báo cáo: {reportedDate}</div>
            </div>
            <div id = "dataTable">
                <Table bordered>
                    <tbody>
                        <tr>
                            {lcrBoardData.columnNames.map(col => <td className='table-title'>{col}</td>)}
                        </tr>
                        {lcrBoardData.sections.map(sec => 
                            <>                                
                                <tr>
                                    <td className='sectionNameTd'>{sec.sectionName}</td>
                                    <td className='sectionNameTd'>{sec.sectionNameVn}</td>
                                    <td className='sectionNameTd'></td>
                                </tr>
                                {sec.rows.map(row => 
                                    <tr>
                                        <td>{row[0]}</td>
                                        <td>{row[1]}</td>
                                        <td>{row[2]}</td>
                                    </tr>
                                )}
                            </>
                        )}
                    </tbody>
                </Table>
            </div>
        </div>
    )
}
