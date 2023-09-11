import { useEffect, useState } from 'react'
import { Button, Form, Stack, Table, Modal } from 'react-bootstrap';
import './viewMappingAndRegulatory.css'
import { getNonDataTable, getNonDataTableList, uploadFile } from '../../../services/calculationToolService';
import useLocalStorageAuth from '../../../hooks/useLocalStorageAuth';

export default function ViewMappingAndRegulatory() {
    const {getAuth} = useLocalStorageAuth()
    const auth = getAuth()
    const [tableType, setTableType] = useState()
    const [tableName, setTableName] = useState()
    const [tableNameOptions, setTableNameOptions] = useState([])
    const [allOptions, setAllOptions] = useState()
    const [tableData, setTableData] = useState()
    const [message, setMessage] = useState('');

    const [uploadChecked, setUploadChecked] = useState(false);
    const [viewChecked, setViewChecked] = useState(true);

    const handleUploadChange = () => {
        setUploadChecked(!uploadChecked);
        setViewChecked(false);
    };

    const handleViewChange = () => {
        setViewChecked(!viewChecked);
        setUploadChecked(false);
    };

    const [showMessagePopup, setShowMessagePopup] = useState(false);
    const handleCloseMessagePopup = () => setShowMessagePopup(false);

    useEffect(() => {
        const fetchOptions = async () => {
            try {
              const options = await getNonDataTableList();
              setAllOptions(options)
            } catch (error) {
              console.error('Error fetching table list', error);
            }
        };
        fetchOptions()
    }, [])

    const handleChangeTableType = (event) => {
        switch (String(event.target.value)) {
            case "mapping":
                setTableNameOptions(allOptions.mapping_tables)
                break;
            case "regulatory":
                setTableNameOptions(allOptions.regulatory_tables)
                break;
            case "others":
                setTableNameOptions(allOptions.other_tables)
                break;
            default:
                setTableNameOptions([])
                break;
        }
    }

    const handleFetchTable = () => {
        const fetchData = async () => {
            try {
              const tableData = await getNonDataTable(tableName)
              setTableData(tableData)
              console.log(tableData)
            } catch (error) {
              console.error('Error fetching table list', error);
            }
        };
        fetchData()
    }

    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
      
        if (file) {
          const reader = new FileReader();
          reader.readAsBinaryString(file); // Read the file as binary
        }
    };

    const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const year = date.getFullYear();
        
        return `${year}-${month}-${day}`;
    }

    const handleUploadFile = async (event) => {
        event.preventDefault();
        const data = {
            fileType: "csv",
            separationSymbol: ",",
            username: auth.username,
            file: selectedFile, 
            tableName: tableName,
            uploadDate: formatDate(new Date())
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
        <Stack gap={3} className='forms-container'>
            <div className="form-input">
                <Form.Label>Chọn loại bảng</Form.Label>
                <Form.Select required onChange={(event) => {
                    handleChangeTableType(event)
                }}>
                    <option >Chọn 1 trong 3 loại bảng</option>
                    <option value={"mapping"}>Bảng Mapping</option>
                    <option value={"regulatory"}>Bảng Regulatory</option>
                    <option value={"others"}>Các bảng khác</option>
                </Form.Select>
            </div>
            <div className="form-input">
                <Form.Label>Chọn bảng</Form.Label>
                <Form.Select required onChange={(event) => {
                    setTableName(String(event.target.value))
                }}>
                    <option >Chọn tên bảng</option>
                    {tableNameOptions.map((x, index) => (
                        <option key={index} value={x}>{x}</option>
                    ))}
                </Form.Select>
            </div>
            <div className="form-input">
                <Form.Check
                    type="checkbox"
                    label="Xem bảng"
                    checked={viewChecked}
                    onChange={handleViewChange}
                />
                <Form.Check
                    type="checkbox"
                    label="Tải bảng lên"
                    checked={uploadChecked}
                    onChange={handleUploadChange}
                />
            </div>
            {viewChecked && <Button onClick={handleFetchTable}>Lấy dữ liệu của bảng</Button>}
            {uploadChecked && 
                <>
                <div className="form-input">
                    <Form.Label>Chọn file dữ liệu</Form.Label>
                    <Form.Control type="file" required  onChange={handleFileInputChange} />
                </div>
                <Button onClick={handleUploadFile}>Tải bảng lên</Button>
                </>
            }
        </Stack>
        <div id='dataTable'>
            <Table striped bordered>
                <tr>
                    {tableData && tableData.columns.map(col => (
                        <td className='table-title'>{col}</td>
                    ))}
                </tr>
                <tbody>
                    {tableData && tableData.data.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <td key={cellIndex}>{cell}</td>
                        ))}
                        </tr>
                    ))}
                </tbody>
            </Table> 
        </div>
        </>
    )
}