import { Table, Row, Col, Button, Form, FormLabel, Stack} from 'react-bootstrap';
import { useEffect, useState, useRef } from "react";
import '../../../Global.css'
import './dashboard.css'
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { getBarChartData } from '../../../services/calculationToolService';

import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

import { Bar } from 'react-chartjs-2';

import { getDashboardLcrNsfrData } from '../../../services/calculationToolService';

export default function CalulationQuickDashboard() {
    const [lcrData, setLcrData] = useState()
    const [nsfrData, setNsfrData] = useState()

    const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const year = date.getFullYear();
        
        return `${day}-${month}-${year}`;
    }
    const currentDate = new Date();
    const formattedDate = formatDate(currentDate);
    const [reportingDate, setReportingDate] = useState(formattedDate)

    useEffect(() => {
        handleFetchReportedData()
    }, []);
    

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

        pdf.save('dashboard-data.pdf');
    };

    const exportToExcel = () => {
        const workbook = XLSX.utils.book_new();
        tableRefs.forEach((tableRef, index) => {
          const worksheet = XLSX.utils.table_to_sheet(tableRef.current);
          XLSX.utils.book_append_sheet(workbook, worksheet, `Sheet${index + 1}`);
        });
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const data = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(data, 'dashboard.xlsx');
    };

    const handleFetchReportedData = () => {
        const fetchLcrNsfr = async () => {
            try {
                const lcrNsfrDat = await getDashboardLcrNsfrData(reportingDate)
                setLcrData(lcrNsfrDat.lcr_data)
                setNsfrData(lcrNsfrDat.nsfr_data)
                const barChartData = await getBarChartData()
                setSetOfDataForFieldStatsBar(barChartData)
            } catch (error) {
              console.error('Error fetching data:', error);
            }
        };
        fetchLcrNsfr()
    }

    // Bar charts
    const [setOfDataForFieldStatsBar, setSetOfDataForFieldStatsBar] = useState([])


    const getBarChartOptions = (title) => {
        return {
            maintainAspectRatio: false,
            scales: {
                y: {
                    maxBarThickness: 1 / 3, // Adjust as needed (proportion of 2/3)
                },
            },
            plugins: {
                title: {
                    display: true,
                    text: title, // Use the title prop here
                    fontSize: 20,
                },
            },
        };
    }

    return (
        <div>
            <div className="chart-container">
                {setOfDataForFieldStatsBar && setOfDataForFieldStatsBar.map(data => 
                    <div className="chart">
                        <Bar data={data} options={getBarChartOptions(data.title)}></Bar>
                    </div>
                )}
            </div>
            <div id="dashboard-general-info">
                <Stack gap={2}>
                    <FormLabel style={{fontWeight:'bold', fontSize:'larger'}}>Chọn ngày báo cáo</FormLabel>
                    <Form.Control 
                        required type="date" 
                        onChange={(event) => {
                            setReportingDate(String(event.target.value))
                        }}/>
                    <div class="button-container">
                        <Button onClick={handleFetchReportedData}>Lấy kết quả tổng quan</Button>    
                    </div>
                </Stack>
            </div>
            <div className='tables-grid'>
                <Row className='pb-4'>
                    <div class="button-container">
                        <Button onClick={handleExportPDF}>Xuất kết quả ra PDF</Button>
                        <Button onClick={exportToExcel}>Xuất kết quả ra Excel</Button>
                    </div>
                </Row>
                <Row className='pb-4'>
                    <Col>
                        <Table striped bordered ref={tableRefs[0]}>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>Liquidity Coverage Ratio - Tỷ lệ đảm bảo khả năng thanh khoàn</td>
                                </tr>
                                {lcrData && lcrData.rows.map(row => 
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
                        <Table striped bordered ref={tableRefs[1]}>
                                <tbody>
                                    <tr>
                                        <td className='table-title' colSpan={2}>Net Stable Funding Ratio - Tỷ lệ quỹ ổn định ròng</td>
                                    </tr>
                                    {nsfrData && nsfrData.rows.map(row => 
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