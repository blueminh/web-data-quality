import { Container, Row, Col, Form, Table, Button, Stack, Modal} from 'react-bootstrap';
import '../../../Global.css'
import './inputboard.css'
import { useState, useContext, useEffect } from 'react';
import AuthContext from '../../../contexts/AuthProvider';
import { fetchUploadHistory, uploadFile } from '../../../services/calculationToolService';
import Autosuggest from 'react-autosuggest';
import * as XLSX from 'xlsx'; // Import xlsx library


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
        tableName: '',
        selectedFile: null,
      });
        
    const fileTypes = ['CSV', 'JSON', 'XML', "EXCEL"];
    const separationSymbols = [',', ';', '|'];
    const [selectedFile, setSelectedFile] = useState(null);
    const [sampleViewData, setSampleViewData] = useState([]);
    const [numColumns, setNumColumns] = useState(0);
    const [message, setMessage] = useState('');

    // suggestion logic for table name
    // list of suggested table names
    const [tableNameOptions, ] = useState([
        'customers',
        'orders',
        'products',
        'employees',
        'suppliers',
    ]);
    const [tableName, setTableName] = useState('');
    const [tableSuggestions, setTableSuggestions] = useState([]);
    const getTableSuggestions = (inputValue) => {
        if (inputValue === ""){
            return tableNameOptions
        }
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = tableNameOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };

    const handleFileTypeChange = (event) => {
        setFormData({ ...formData, fileType: String(event.target.value)});
    };

    const handleSeparationSymbolChange = (event) => {
        setFormData({ ...formData, separationSymbol: String(event.target.value)});
    };

    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
      
        if (file) {
          const reader = new FileReader();
          
          reader.onload = (e) => {
            const content = e.target.result;
      
            if (file.name.endsWith('.csv')) {
              // Handle CSV file
              const rows = content.split('\n'); // Split content into rows
              const firstFiveRows = rows.slice(0, 5); // Get the first 5 rows
          
              // Convert rows to an array of arrays (cells)
              const parsedData = firstFiveRows.map((row) => row.split(','));
          
              setSampleViewData(parsedData);
      
              // Get the number of columns from the first row (header row)
              const numCols = parsedData[0] ? parsedData[0].length : 0;
              setNumColumns(numCols);
            } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
              // Handle Excel file
              const workbook = XLSX.read(content, { type: 'binary' });
              const firstSheetName = workbook.SheetNames[0];
              const worksheet = workbook.Sheets[firstSheetName];
              const parsedData = XLSX.utils.sheet_to_json(worksheet, { header: 1, range: 5 });
      
              setSampleViewData(parsedData);
      
              // Get the number of columns from the first row
              const numCols = parsedData[0] ? parsedData[0].length : 0;
              setNumColumns(numCols);
            } else {
              // Handle unsupported file types
              console.log('Unsupported file type');
            }
          };
      
          reader.readAsBinaryString(file); // Read the file as binary
        }
      };


    useEffect(() => {
        const fetchHistory = async () => {
            try {
              const history = await fetchUploadHistory(auth.username);
              setUploadHistory(history);
            } catch (error) {
              console.error('Error fetching upload history:', error);
            }
        };
      
        fetchHistory();
    }, []);


    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();
        formData.append('username', auth.username);
        formData.append('file', selectedFile);
    
        try {
            const message = await uploadFile(auth.username, selectedFile);
            setMessage(message);
            setShow(true);
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('An error occurred while uploading the file.');
        }
        setShow(true)
    };

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    
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
            </Modal>
            <Container fluid>
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
                            {formData.fileType === "CSV" &&                             
                            <div className="form-input">
                                <Form.Label>Select separation symbol</Form.Label>
                                <Form.Select required onChange={handleSeparationSymbolChange}>
                                    {separationSymbols.map(type => <option>{type}</option>)}
                                </Form.Select>
                            </div>}
                            <div className="form-input">
                                <Form.Label>Table name</Form.Label>
                                <Autosuggest
                                    suggestions={tableSuggestions}
                                    onSuggestionsFetchRequested={({ value }) => {
                                        setTableSuggestions(getTableSuggestions(value, ));  
                                    }}
                                    onSuggestionsClearRequested={() => setTableSuggestions([])}
                                    onSuggestionSelected={(event, { suggestion }) => {
                                        setTableName(suggestion);
                                        setFormData({ ...formData, tableName: suggestion });
                                    }}
                                    getSuggestionValue={(suggestion) => suggestion}
                                    renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                    inputProps={{
                                        placeholder: 'Start typing to search...',
                                        value: tableName,
                                        onChange: (event, { newValue }) => {
                                            setTableName(newValue);
                                            setFormData({ ...formData, tableName: newValue });
                                        },
                                    }}
                                />
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
                                        {sampleViewData.map((row, rowIndex) => (
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
                    <Col>
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
                    </Col>
                </Row>
            </Container>
        </>
        
    )
}