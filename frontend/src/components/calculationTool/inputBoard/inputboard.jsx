import { Container, Row, Col, Form, Table, Button, Stack, Modal} from 'react-bootstrap';
import '../../../Global.css'
import './inputboard.css'
import { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import AuthContext from '../../../contexts/AuthProvider';

export default function InputDashboard() {
    const {auth} = useContext(AuthContext)
    const [uploadHistory, setUploadHistory] = useState([
            ["27/07/2023", "data.csv"],
            ["27/07/2023", "data.csv"],
            ["27/07/2023", "data.csv"]
        ]
    )

    const [formData, setFormData] = useState({
        fileType: '',
        separationSymbol: '',
        selectedFile: null,
      });
        
    const fileTypes = ['CSV', 'JSON', 'XML'];
    const separationSymbols = [',', ';', '|'];
    const [csvData, setCsvData] = useState([]);
    const [numColumns, setNumColumns] = useState(0);

    const [message, setMessage] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileTypeChange = (selectedFileType) => {
        setFormData({ ...formData, fileType: selectedFileType });
    };

    const handleSeparationSymbolChange = (selectedSymbol) => {
        setFormData({ ...formData, separationSymbol: selectedSymbol });
    };

    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file)
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


    useEffect(() => {
      const fetchUploadHistory = async () => {
        try {
          const response = await axios.get(`http://localhost:8085/upload/history?username=${auth.username}`, {
            withCredentials: true
          });
          setUploadHistory(response.data.upload_history);
        } catch (error) {
          console.error('Error fetching upload history:', error);
        }
      };
  
      fetchUploadHistory();
    }, []);


    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();
        formData.append('username', auth.username);
        formData.append('file', selectedFile);
    
        try {
          const response = await axios.post('http://localhost:8085/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            withCredentials: true 
          });
          
          setMessage(response.data.message);
        } catch (error) {
          setMessage('An error occurred while uploading the file.');
        }
        setShow(true)
    };

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    
    const formatTimestamp = (inputTimestamp) => {
        const date = new Date(inputTimestamp);
        const day = date.getDate();
        const month = date.getMonth() + 1; // Months are zero-indexed
        const year = date.getFullYear();
        const hours = date.getHours();
        const minutes = date.getMinutes();
    
        const formattedDate = `${day}/${month}/${year}`;
        const formattedTime = `${hours}:${minutes}`;
    
        return `${formattedDate} ${formattedTime}`;
    }

    return (
        <>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>Upload Status</Modal.Title>
                </Modal.Header>
                <Modal.Body>{message}</Modal.Body>
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
                            <Button onClick={handleSubmit}>Submit file</Button>
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
                                    <td className='table-title' colSpan={2}>{"Lịch sử upload"}</td>
                                </tr>
                                {uploadHistory.map(row => 
                                    <tr>
                                        {<td style={{textAlign: "center"}}>{row.filename}</td>}
                                        {<td style={{textAlign: "center"}}>{row.upload_time}</td>}
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