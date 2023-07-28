import { Container, Row, Col, Form, Table, Button, Stack, Modal} from 'react-bootstrap';
import '../../../Global.css'
import './inputboard.css'
import { useState } from 'react';



export default function InputDashboard() {
    const [uploadHistory, setUploadHistory] = useState({
        title: "Lịch sử upload",
        colNames: ["Ngày", "Tên người upload", "Tên file"],
        rows: [
            ["27/07/2023", "Hoang Minh", "data.csv"],
            ["27/07/2023", "Hoang Minh", "data.csv"],
            ["27/07/2023", "Hoang Minh", "data.csv"]
        ]
    })

    const [formData, setFormData] = useState({
        fileType: '',
        separationSymbol: '',
        selectedFile: null,
      });
    
    const fileTypes = ['CSV', 'JSON', 'XML'];
    const separationSymbols = [',', ';', '|'];
    const [csvData, setCsvData] = useState([]);
    const [numColumns, setNumColumns] = useState(0);



    const handleFileTypeChange = (selectedFileType) => {
        setFormData({ ...formData, fileType: selectedFileType });
    };

    const handleSeparationSymbolChange = (selectedSymbol) => {
        setFormData({ ...formData, separationSymbol: selectedSymbol });
    };

    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
    
        reader.onload = (e) => {
          const csvContent = e.target.result;
          const rows = csvContent.split('\n'); // Split content into rows
          const firstFiveRows = rows.slice(0, 5); // Get the first 5 rows
    
          // Convert rows to an array of arrays (cells)
          const parsedData = firstFiveRows.map((row) => row.split(','));
    
          setCsvData(parsedData);

          // Get the number of columns from the first row (header row)
            const numCols = parsedData[0] ? parsedData[0].length : 0;
            setNumColumns(numCols);
        };
    
        reader.readAsText(file); // Read the file as text
    };


    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    

    return (
        <>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>Upload Status</Modal.Title>
                </Modal.Header>
                <Modal.Body>Your file has been successfully uploaded</Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                </Modal.Footer>
            </Modal><Container fluid>
            <Row>
                <Col>
                    {/* Content for the left half */}
                    <Stack gap={3}>
                        <div className="form-input">
                            <Form.Label>Select file type</Form.Label>
                            <Form.Select required onChange={handleFileTypeChange}>
                                {fileTypes.map(type => <option>{type}</option>)}
                            </Form.Select>
                        </div>
                        <div className="form-input">
                            <Form.Label>Select separation symbol</Form.Label>
                            <Form.Select required onChange={handleSeparationSymbolChange}>
                                {separationSymbols.map(type => <option>{type}</option>)}
                            </Form.Select>
                        </div>
                        <div className="form-input">
                            <Form.Label>Choose file</Form.Label>
                            <Form.Control type="file" required  onChange={handleFileInputChange} />
                        </div>
                        <div>
                            <Button onClick={handleShow}>Submit file</Button>
                        </div>
                        <Table striped bordered>
                                <tr>
                                    <td className='table-title' colSpan={numColumns}>Sample View</td>
                                </tr>
                                <tbody>
                                    {csvData.map((row, rowIndex) => (
                                        <tr key={rowIndex}>
                                        {row.map((cell, cellIndex) => (
                                            <td key={cellIndex}>{cell}</td>
                                        ))}
                                        </tr>
                                    ))}
                                </tbody>
                        </Table>      
                    </Stack>
                </Col>
                <Col xs={3}>
                    {/* Content for the right half */}
                    <div>
                        <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={3}>{uploadHistory.title}</td>
                                </tr>
                                {uploadHistory.rows.map(row => 
                                    <tr>
                                        {row.map(rowData =>
                                            <td style={{textAlign: "center"}}>{rowData}</td>
                                        )}
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    </div>
                </Col>
            </Row>
        </Container>
        </>
        
    )
}