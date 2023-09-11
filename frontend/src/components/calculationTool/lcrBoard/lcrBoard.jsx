import { useState, useRef } from 'react'
import { Table, Button, Form, FormLabel, Stack, Spinner, Modal } from 'react-bootstrap';
import './lcrBoard.css'

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import { calculateLcr, getCalculatedData } from '../../../services/calculationToolService';
import ExpandableRow from '../../expandableRow/expandableRow';
import { lcrBoardDataDefault } from './defaultValues';
import ChooseFileDateDialog from '../chooseFileDateDialog/chooseFileDateDialog';

export default function LCRDashBoard() {
     // eslint-disable-next-line
     const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const year = date.getFullYear();
        
        return `${year}-${month}-${day}`;
    }
    const currentDate = new Date();
    const formattedDate = formatDate(currentDate);
    const [reportingDate, setReportingDate] = useState(formattedDate)
    const [extraTables, setExtraTables] = useState({})
 
    const [isLoading, setIsLoading] = useState(false);

     // eslint-disable-next-line
    const [lcrBoardData, setLcrBoardData] = useState(lcrBoardDataDefault)

    const [showChooseFileDateDialog, setShowChooseFileDateDialog] = useState(false);
    const modalChooseFileDateDialogToggle = () => setShowChooseFileDateDialog(!showChooseFileDateDialog)

    const [showMessagePopup, setShowMessagePopup] = useState(false);
    const handleCloseMessagePopup = () => setShowMessagePopup(false);
    const [errorMessage, setErrorMessage] = useState("")

    const handleCalculateLcr = (requestData) => {
        const fetchLcr = async () => {
            try {
                setIsLoading(true)
                const response = await calculateLcr(requestData)
                setIsLoading(false)

                if (response.success) {
                    setLcrBoardData(response.data)
                    setIsLoading(false)
                    setShowChooseFileDateDialog(false)
                } else {
                    setExtraTables(response.extraTables)
                    setShowChooseFileDateDialog(true)
                }
            } catch (error) {
                setLcrBoardData(lcrBoardDataDefault)
                setIsLoading(false)
                console.error('Error fetching data:', error);
            }
        };
        fetchLcr()
    }

    const handleFetchCalculatedLcr = () => {
        const fetchLcr = async () => {
            try {
                const response = await getCalculatedData(reportingDate, "lcr")
                if (response.success) {
                    setLcrBoardData(response.data)
                } else {
                    setErrorMessage(response.error)
                    setShowMessagePopup(true)
                }
            } catch (error) {
                setErrorMessage("Có lỗi đã xảy ra")
                setShowMessagePopup(true)
            }
        };
        fetchLcr()
    }

    const tableRefs = [useRef(null)];
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
              const imgWidth = 190; // Width of the image (in mm)
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

        pdf.save('lcr-data.pdf');
    };

    const exportToExcel = () => {
        const workbook = XLSX.utils.book_new();
        tableRefs.forEach((tableRef, index) => {
          const worksheet = XLSX.utils.table_to_sheet(tableRef.current);
          XLSX.utils.book_append_sheet(workbook, worksheet, `Sheet${index + 1}`);
        });
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const data = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(data, 'lcr.xlsx');
    };

    return (
        <>
        {showChooseFileDateDialog && <ChooseFileDateDialog  
            onCloseHandle={modalChooseFileDateDialogToggle}
            reportingDate={reportingDate}
            extraTables={extraTables}
            onSubmitHandle={handleCalculateLcr}
        />}
        <Modal show={showMessagePopup} onHide={handleCloseMessagePopup}>
            <Modal.Header closeButton>
                <Modal.Title>Lỗi</Modal.Title>
            </Modal.Header>
            <Modal.Body>{errorMessage}</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseMessagePopup}>
                    Đóng
                </Button>
            </Modal.Footer>
        </Modal>
        <div>
            <div id = "pageTitle">NAB - Basel III Tỷ lệ bao phủ thanh khoản (LCR) - Công bố thông tin (Public Discloure)</div>
            <div id = "generalInfo">
                <Stack gap={2}>
                    <FormLabel style={{fontWeight:'bold', fontSize:'larger'}}>Chọn ngày báo cáo</FormLabel>
                    <Form.Control
                        value={reportingDate} 
                        required type="date" 
                        onChange={(event) => {
                            setReportingDate(String(event.target.value))
                        }}/>
                    <div className="button-container">
                        {isLoading && <Spinner />}
                        <Button onClick={() => handleCalculateLcr({
                                "reportingDate":reportingDate,
                                "extraTables":{}
                            })}>Tính toán
                        </Button>
                        <Button onClick={handleFetchCalculatedLcr}>Lấy kết quả</Button>     
                        <Button onClick={handleExportPDF}>Export to PDF</Button>
                        <Button onClick={exportToExcel}>Export to Excel</Button>
                    </div>
                </Stack>
            </div>
            <div id="dataTable" className="table-responsive">
                <Table bordered>
                    <tbody>
                        <tr>
                            {["No.", "Item", "Khoản mục", "Total unweighted value", "Total weighted value"].map(col => <td className='table-title'>{col}</td>)}
                        </tr>
                        {lcrBoardData.map(row => <ExpandableRow row={row}></ExpandableRow>)}
                    </tbody>
                </Table>
            </div>
        </div>
        </>
    )
}
