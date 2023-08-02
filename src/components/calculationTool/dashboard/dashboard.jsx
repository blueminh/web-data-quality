import { Table, Row, Col, Button } from 'react-bootstrap';
import { useEffect, useState, useRef } from "react";
import '../../../Global.css'
import './dashboard.css'
import FetchDataService from '../../../services/fetchDataService'
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export default function CalulationQuickDashboard() {
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

    const tableRefs = [useRef(null), useRef(null)];
    const handleExportPDF = async () => {
        const pdf = new jsPDF('p', 'mm', 'a4');
    
        let currentPage = 1;
        let currentY = 15; // Starting position for the first table (in mm)
    
        const availableHeight = 265; // Total available height on each page (in mm)
        const marginBottom = 10; // Space between tables (in mm)
        for (let i = 0; i < tableRefs.length; i++) {
            const tableRef = tableRefs[i];
            if (tableRef.current) {
              const canvas = await html2canvas(tableRef.current);
              const imgData = canvas.toDataURL('image/png');
              const imgWidth = 150; // Width of the image (in mm)
              const imgHeight = (canvas.height * imgWidth) / canvas.width; // Calculate height based on aspect ratio
      
              // Check if the current table fits on the current page
              if (currentY + imgHeight > availableHeight && i > 0) {
                pdf.addPage();
                currentPage++;
                currentY = 15; // Reset the starting position for the next page
              }


                // Add the table at the specified position
                pdf.addImage(imgData, 'PNG', 10, currentY, imgWidth, imgHeight);

                // Update the current position for the next table
                currentY += imgHeight + marginBottom;
            }
        }

        pdf.save('exported-tables.pdf');
    };


    return (
        <div>
            <div id="dashboard-general-info">
                <Row style={{fontWeight:'bold', fontSize:'larger'}}>
                    <Col>CAO</Col>
                    <Col>{formattedDate}</Col>
                </Row>
            </div>
            <div className='tables-grid'>
                <Row>
                    <Col>
                        <Table striped bordered ref={tableRefs[0]}>
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
                        <Button onClick={handleExportPDF}>Export to PDF</Button>
                    </Col>
                    <Col>
                    <Table striped bordered ref={tableRefs[1]}>
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