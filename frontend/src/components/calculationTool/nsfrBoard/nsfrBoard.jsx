import { useState, useRef } from 'react'
import { Table, Button, Form, FormLabel, Stack, Spinner, Modal } from 'react-bootstrap';
import './nsfrBoard.css'

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import { calculateNsfr, getCalculatedData } from '../../../services/calculationToolService';
import ExpandableRow from '../../expandableRow/expandableRow';
import { nsfrBoardDataDefault } from './defaultValues';
import ChooseFileDateDialog from '../chooseFileDateDialog/chooseFileDateDialog';

export default function NSFRDashBoard() {
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
     const processBoardRow = (row) => {
        // console.log(row.data.filter((_, index) => index !== 1))
        const newRow = {
            ...row,
            data: row.data.filter((_, index) => index !== 1).map((item, index) => {
                if (index == 0) {
                    return item
                }
                if (typeof item !== 'number') {
                    return item; // Return non-numeric items as-is
                }
                if (item == 0 ) {
                    return 0
                } else if (item > 1000) {
                  // Convert large numbers to integers with commas
                  return item.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                } else if (item < 3) {
                  // Round small numbers to 2 decimal points
                  return item.toFixed(2);
                } else {
                  return item;
                }
            }),
            children: row.children.map((child) => processBoardRow(child))
        }
        return newRow
    }

    const processBoardData = (data) => { 
        return data.map((row) => processBoardRow(row))
    }  
    const [nsfrBoardData, setNsfrBoardData] = useState(processBoardData(nsfrBoardDataDefault))

    const [showChooseFileDateDialog, setShowChooseFileDateDialog] = useState(false);
    const modalChooseFileDateDialogToggle = () => setShowChooseFileDateDialog(!showChooseFileDateDialog)

    const [showMessagePopup, setShowMessagePopup] = useState(false);
    const handleCloseMessagePopup = () => setShowMessagePopup(false);
    const [errorMessage, setErrorMessage] = useState("")

    const handleCalculateNsfr = (requestData) => {
        const fetchNsfr = async () => {
            try {
                setIsLoading(true)
                const response = await calculateNsfr(requestData)
                setIsLoading(false)

                if (response.success) {
                    setNsfrBoardData(processBoardData(response.data))
                    setIsLoading(false)
                    setShowChooseFileDateDialog(false)
                } else {
                    setExtraTables(response.extraTables)
                    setShowChooseFileDateDialog(true)
                }
            } catch (error) {
                setNsfrBoardData(processBoardData(nsfrBoardDataDefault))
                setIsLoading(false)
                console.error('Error fetching data:', error);
            }
        };
        fetchNsfr()
    }

    const handleFetchCalculatedNsfr = () => {
        const fetchNsfr = async () => {
            try {
                const response = await getCalculatedData(reportingDate, "nsfr")
                if (response.success) {
                    setNsfrBoardData(processBoardData(response.data))
                } else {
                    setErrorMessage(response.error)
                    setShowMessagePopup(true)
                }
            } catch (error) {
                setErrorMessage("Có lỗi đã xảy ra")
                setShowMessagePopup(true)
            }
        };
        fetchNsfr()
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
            onSubmitHandle={handleCalculateNsfr}
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
            <div id = "pageTitle">NSFR</div>
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
                        <Button onClick={() => handleCalculateNsfr({
                                "reportingDate":reportingDate,
                                "extraTables":{}
                            })}>Tính toán
                        </Button>    
                        <Button onClick={handleFetchCalculatedNsfr}>Lấy kết quả</Button>
                        <Button onClick={handleExportPDF}>Export to PDF</Button>
                        <Button onClick={exportToExcel}>Export to Excel</Button>
                    </div>
                </Stack>
            </div>
            <div id="dataTable" className="table-responsive">
                <Table bordered>
                    <tbody>
                        <tr>
                            {["No.", "Khoản mục", "","","","",""].map(col => <td className='table-title'>{col}</td>)}
                        </tr>
                        {nsfrBoardData.map(row => <ExpandableRow row={row}></ExpandableRow>)}
                    </tbody>
                </Table>
            </div>
        </div>
        </>
    )
}
