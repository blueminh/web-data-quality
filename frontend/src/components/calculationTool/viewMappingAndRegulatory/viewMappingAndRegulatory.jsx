import { useEffect, useState } from 'react'
import { Button, Form, Stack, Table } from 'react-bootstrap';
import './viewMappingAndRegulatory.css'
import { getNonDataTable, getNonDataTableList } from '../../../services/calculationToolService';

export default function ViewMappingAndRegulatory() {
    const [tableType, setTableType] = useState()
    const [tableName, setTableName] = useState()
    const [tableNameOptions, setTableNameOptions] = useState([])
    const [allOptions, setAllOptions] = useState()
    const [tableData, setTableData] = useState()
    const [numColumns, setNumColumns] = useState(3);

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

    const handleSubmit = () => {
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

    return (
        <>
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
                    {tableNameOptions.map((x, index) => (
                        <option key={index} value={x}>{x}</option>
                    ))}
                </Form.Select>
            </div>
            <Button onClick={handleSubmit}>Lấy dữ liệu của bảng</Button>
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