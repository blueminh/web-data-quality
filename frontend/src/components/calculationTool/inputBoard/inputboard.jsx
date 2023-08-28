import { Container, Row, Col, Form, Table, Button, Stack, Modal} from 'react-bootstrap';
import '../../../Global.css'
import './inputboard.css'
import { useState, useEffect } from 'react';
import { fetchUploadHistory, uploadFile } from '../../../services/calculationToolService';
import Autosuggest from 'react-autosuggest';
import * as XLSX from 'xlsx'; // Import xlsx library
import useLocalStorageAuth from '../../../hooks/useLocalStorageAuth'
import { getTableList } from '../../../services/calculationToolService';


export default function InputDashboard() {
    const {getAuth} = useLocalStorageAuth()
    const auth = getAuth()
    const [uploadHistory, setUploadHistory] = useState([
            ["27/07/2023", "data.csv"],
            ["27/07/2023", "data.csv"],
            ["27/07/2023", "data.csv"]
        ]
    )

        
    const fileTypes = ['csv', 'json', "xlsx", "xls"];
    const [fileTyle, setFileType] = useState("csv")
    const separationSymbols = [',', ';', '|'];
    const [separationSymbol, setSeparationSymbol] = useState(',')
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewData, setPreviewData] = useState([]);
    const [numColumns, setNumColumns] = useState(0);
    const [message, setMessage] = useState('');

    // suggestion logic for table name
    // list of suggested table names
    const [tableNameOptions, setTableNameOptions] = useState([
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

    // suggestion logic for regulatory table
    // list of suggested regulatory table
    const [regulatoryTableOptions, ] = useState([
        'r1',
        'r2'
    ]);
    const [regulatoryTable, setRegulatoryTable] = useState('');
    const [regulatoryTableSuggestions, setRegulatoryTableSuggestions] = useState([]);
    const getRegulatoryTableSuggestions = (inputValue) => {
        if (inputValue === ""){
            return regulatoryTableOptions
        }
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = regulatoryTableOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };

    // suggestion logic for table mapping name
    // list of suggested table mapping names
    const [tableMappingNameOptions, ] = useState([
        'customers m',
        'orders m',
        'products',
        'employees',
        'suppliers',
    ]);
    const [tableMappingName, setTableMappingName] = useState('');
    const [tableMappingSuggestions, setTableMappingSuggestions] = useState([]);
    const getTableMappingSuggestions = (inputValue) => {
        if (inputValue === ""){
            return tableNameOptions
        }
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = tableMappingNameOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };

    const [sampleData, setSampleData] = useState([
        ["Jack","McGinnis","220 hobo Av.","Phila"," PA",9119  ],
        ["John \"Da Man\"","Repici","120 Jefferson St.","Riverside"," NJ",8075  ],
        ["Stephen","Tyler","7452 Terrace \"At the Plaza\" road","SomeTown","SD",91234  ],
        ["","Blankman","","SomeTown"," SD",298  ],
        ["Joan \"the bone\", Anne","Jet","9th, at Terrace plc","Desert City","CO",123  ]
    ])
    const [isOpenAddGrant, setOpenAddGrant] = useState(false)
    const [showSampleDataPopup, setShowSampleDataPopup] = useState(false);
    const handleCloseSampleDataPopup = () => setShowSampleDataPopup(false);

    const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const year = date.getFullYear();
        
        return `${year}-${month}-${day}`;
    }
    const currentDate = new Date();
    const formattedDate = formatDate(currentDate);
    const [uploadDate, setUploadDate] = useState(formattedDate)


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
          
              setPreviewData(parsedData);
      
              // Get the number of columns from the first row (header row)
              const numCols = parsedData[0] ? parsedData[0].length : 0;
              setNumColumns(numCols);
            } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
              // Handle Excel file
              const workbook = XLSX.read(content, { type: 'binary' });
              const firstSheetName = workbook.SheetNames[0];
              const worksheet = workbook.Sheets[firstSheetName];
              const parsedData = XLSX.utils.sheet_to_json(worksheet, { header: 1, range: 5 });
      
              setPreviewData(parsedData);
      
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

        const fetchTableOptions = async () => {
            try {
              const tableOptions = await getTableList()
              setTableNameOptions(tableOptions)
            } catch (error) {
              console.error('Error fetching table list', error);
            }
        };
      
        fetchHistory();
        fetchTableOptions()
    }, []);


    const handleSubmit = async (event) => {
        event.preventDefault();
        const data = {
            fileType: fileTyle,
            separationSymbol: separationSymbol,
            username: auth.username,
            file: selectedFile, 
            tableName: tableName,
            uploadDate: uploadDate
        }
        try {
            const message = await uploadFile(data);
            setMessage(message);
            setShowMessagePopup(true);
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Tải file không thành công');
            setShowMessagePopup(true)
        }
    };

    const [showMessagePopup, setShowMessagePopup] = useState(false);
    const handleCloseMessagePopup = () => setShowMessagePopup(false);
    
    return (
        <>
            <Modal show={showMessagePopup} onHide={handleCloseMessagePopup}>
                <Modal.Header closeButton>
                    <Modal.Title>Trạng thái tải lên</Modal.Title>
                </Modal.Header>
                <Modal.Body>{message}</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseMessagePopup}>
                        Đóng
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal dialogClassName="dialog-tool-wide" show={showSampleDataPopup} onHide={handleCloseSampleDataPopup}>
                <Modal.Header closeButton>
                    <Modal.Title>Dữ liệu mẫu của bảng đã chọn</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {tableName === ""
                        ? "Vui lòng chọn bảng"
                        : <Table striped bordered>
                            <tbody>
                                {sampleData.map((row, rowIndex) => (
                                    <tr key={rowIndex}>
                                    {row.map((cell, cellIndex) => (
                                        <td key={cellIndex}>{cell}</td>
                                    ))}
                                    </tr>
                                ))}
                            </tbody>
                        </Table>      
                    }
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseSampleDataPopup}>
                        Đóng
                    </Button>
                </Modal.Footer>
            </Modal>
            <Container fluid>
                <Row>
                    <Col>
                        {/* Content for the left half */}
                        <Stack gap={3}>
                            <div className="form-input">
                                <Form.Label>Chọn bảng dữ liệu cần nhập</Form.Label>
                                <Autosuggest
                                    suggestions={tableSuggestions}
                                    onSuggestionsFetchRequested={({ value }) => {
                                        setTableSuggestions(getTableSuggestions(value, ));  
                                    }}
                                    onSuggestionsClearRequested={() => setTableSuggestions([])}
                                    onSuggestionSelected={(event, { suggestion }) => {
                                        setTableName(suggestion);
                                    }}
                                    getSuggestionValue={(suggestion) => suggestion}
                                    renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                    inputProps={{
                                        placeholder: 'Start typing to search...',
                                        value: tableName,
                                        onChange: (event, { newValue }) => {
                                            setTableName(newValue);
                                        },
                                    }}
                                />
                            </div>
                            <div className='centered-button-container'>
                                <Button onClick={() => setShowSampleDataPopup(true)}>Bấm để xem dữ liệu mẫu của bảng đã chọn</Button>
                            </div>
                            {/* <div className="form-input">
                                <Form.Label>Chọn bảng mapping cần nhập</Form.Label>
                                <Autosuggest
                                    suggestions={tableMappingSuggestions}
                                    onSuggestionsFetchRequested={({ value }) => {
                                        setTableMappingSuggestions(getTableMappingSuggestions(value))
                                    }}
                                    onSuggestionsClearRequested={() => setTableMappingSuggestions([])}
                                    onSuggestionSelected={(event, { suggestion }) => {
                                        setTableMappingName(suggestion);
                                    }}
                                    getSuggestionValue={(suggestion) => suggestion}
                                    renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                    inputProps={{
                                        placeholder: 'Start typing to search...',
                                        value: tableMappingName,
                                        onChange: (event, { newValue }) => {
                                            setTableMappingName(newValue);
                                        },
                                    }}
                                />
                            </div>
                            <div className="form-input">
                                <Form.Label>Chọn bảng regulatory cần nhập</Form.Label>
                                <Autosuggest
                                    suggestions={regulatoryTableSuggestions}
                                    onSuggestionsFetchRequested={({ value }) => {
                                        setRegulatoryTableSuggestions(getRegulatoryTableSuggestions(value))
                                    }}
                                    onSuggestionsClearRequested={() => setRegulatoryTableSuggestions([])}
                                    onSuggestionSelected={(event, { suggestion }) => {
                                        setRegulatoryTable(suggestion)
                                    }}
                                    getSuggestionValue={(suggestion) => suggestion}
                                    renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                    inputProps={{
                                        placeholder: 'Start typing to search...',
                                        value: regulatoryTable,
                                        onChange: (event, { newValue }) => {
                                            setRegulatoryTable(newValue)
                                        },
                                    }}
                                />
                            </div>*/}
                            <div className="form-input">
                                <Form.Label>Chọn định dạng file</Form.Label>
                                <Form.Select required onChange={(event) => {
                                    setFileType(String(event.target.value))
                                }}>
                                    {fileTypes.map(type => <option>{type}</option>)}
                                </Form.Select>
                            </div>
                            {fileTyle === "csv" &&                             
                            <div className="form-input">
                                <Form.Label>Chọn kí tự phân cách (đối với file csv)</Form.Label>
                                <Form.Select required onChange={(event) => {
                                    setSeparationSymbol(String(event.target.value))
                                }}>
                                    {separationSymbols.map(type => <option>{type}</option>)}
                                </Form.Select>
                            </div>}
                            <div className="form-input">
                                <Form.Label>Chọn file dữ liệu</Form.Label>
                                <Form.Control type="file" required  onChange={handleFileInputChange} />
                            </div>
                            <div className="form-input">
                                <Form.Label>Chọn ngày</Form.Label>
                                <Form.Control
                                value={uploadDate} 
                                required type="date" 
                                onChange={(event) => {
                                    setUploadDate(String(event.target.value))
                                }}/>                            
                            </div>
                            <div className='centered-button-container'>
                                <Button onClick={handleSubmit}>Tải file lên</Button>
                            </div>
                            <Table striped bordered>
                                    <tr>
                                        <td className='table-title' colSpan={numColumns}>Bản xem thử file đã chọn</td>
                                    </tr>
                                    <tbody>
                                        {previewData.map((row, rowIndex) => (
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