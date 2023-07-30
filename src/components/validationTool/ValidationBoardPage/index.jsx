import {React, useState} from "react";
import {Row, Col, Table, Form, Stack} from 'react-bootstrap';
import Autosuggest from 'react-autosuggest';


import './ValidationPage.css';
import {Pie, Bar} from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale,
    LinearScale,
    BarElement,
    Title,} from 'chart.js';

    ChartJS.register(ArcElement, Tooltip, Legend);
    ChartJS.register(
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend)
    console.log("test")

export default function ValidationDashBoard() {

    const [basicInformation, setBasicInformation] = useState({
        nameOfDatabase: "KPMG",
        dateStart: "xxxx-xx-xx",
        dateEnd: "xxxx-xx-xx",
        tableCheck: ["placeholder1", "placeholder2"],
        tableEliminate: ["placeholder1", "placeholder2"]
    })

    const [dataForPie, setDataForPie] = useState({
        labels: [
          'Bảng Tốt',
          'Bảng Cần Kiểm Tra',
        ],
        datasets: [{
          label: 'Số lượng bảng',
          data: [300, 50],
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      });

    const [setOfDataInBar, setSetOfDataInBar] = useState([{
        fileName: 'Transaction.xls',
        text: 5,
        numeric: 7,
        datetime: 3,
        numberOfLines: 3
      }, 
      {
        fileName: 'Transaction2.xls',
        text: 8,
        numeric: 5,
        datetime: 3,
        numberOfLines: 3
      }]
    )

    const dataForBarChart = (dataInBar) => {
        return {
            labels: ["Text field", "Numeric"],
            datasets: [
                {
                    label: dataInBar.fileName,
                    data: [dataInBar.text, dataInBar.numeric],
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                },
                
                ], 
        }
    }


    const updateStartDate = (event) => { setBasicInformation((prev) => ({
        ...prev,
        dateStart: String(event.target.value)
    }));}

    const updateEndDate = (event) => { setBasicInformation((prev) => ({
        ...prev,
        dateEnd: String(event.target.value)
    }));}

    const refreshPage = (event) => {
        setTimeout(()=>{
            window.location.reload(false);
        }, 500);
        console.log('page to reload')
    }
    
    
    // suggestion logic for database
    const [databaseNameOptions, setDatabaseNameOptions] = useState([
        'KPMG',
        'KPMG 2'
    ]);
    const [databaseName, setDatabaseName] = useState('');
    const [databaseSuggestions, setDatabaseSuggestions] = useState([]);
    const getDatabaseSuggestions = (inputValue) => {
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = databaseNameOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };

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
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = tableNameOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };

    // suggestion logic for excluded table name
    const [excludedTableNameOptions, setExcludedTableNameOptions] = useState([
        'customers',
        'orders',
        'products',
        'employees',
        'suppliers',
    ]);
    const [excludedTableName, setExcludedTableName] = useState('');
    const [excludedTableSuggestions, setExcludedTableSuggestions] = useState([]);
    const getExcludedTableSuggestions = (inputValue) => {
        const inputValueLowerCase = inputValue.trim().toLowerCase();
        const filteredSuggestions = excludedTableNameOptions.filter((name) =>
            name.toLowerCase().includes(inputValueLowerCase)
        );
        return filteredSuggestions;
    };


    // handle file upload
    const [csvData, setCsvData] = useState(null);
    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
    
        reader.onload = (e) => {
          const csvContent = e.target.result;
          setCsvData(csvContent);
        };
    
        reader.readAsText(file); // Read the file as text
    };    

    // handle chossing separation symbol
    const separationSymbols = [',', ';', '|'];
    const [separationSymbol, setSeparationSymbol] = useState(',')
    const handleSeparationSymbolChange = (selectedSymbol) => {
        setSeparationSymbol(selectedSymbol)
    };

    return (
        <>
        <div class="container text-center" style={{marginTop:"20px"}}>
            <Row>
                <Col>
                    <Stack gap={3}>
                        <div className="form-input">
                            <Form.Label>Cơ sở dữ liệu</Form.Label>
                            <Autosuggest
                                suggestions={databaseSuggestions}
                                onSuggestionsFetchRequested={({ value }) => {
                                    setDatabaseSuggestions(getDatabaseSuggestions(value, ));  
                                }}
                                onSuggestionsClearRequested={() => setDatabaseSuggestions([])}
                                onSuggestionSelected={(event, { suggestion }) => {
                                    setDatabaseName(suggestion);
                                }}
                                getSuggestionValue={(suggestion) => suggestion}
                                renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                inputProps={{
                                    placeholder: 'Start typing to search...',
                                    value: databaseName,
                                    onChange: (event, { newValue }) => {
                                        setDatabaseName(newValue);
                                    },
                                }}
                            />
                        </div>
                        <div className="form-input">
                            <Form.Label>Tên bảng cần kiểm tra</Form.Label>
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
                        <div className="form-input">
                            <Form.Label>Tên bảng cần loại trừ</Form.Label>
                            <Autosuggest
                                suggestions={excludedTableSuggestions}
                                onSuggestionsFetchRequested={({ value }) => {
                                    setExcludedTableSuggestions(getExcludedTableSuggestions(value, ));  
                                }}
                                onSuggestionsClearRequested={() => setExcludedTableSuggestions([])}
                                onSuggestionSelected={(event, { suggestion }) => {
                                    setExcludedTableName(suggestion);
                                }}
                                getSuggestionValue={(suggestion) => suggestion}
                                renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                                inputProps={{
                                    placeholder: 'Start typing to search...',
                                    value: excludedTableName,
                                    onChange: (event, { newValue }) => {
                                        setExcludedTableName(newValue);
                                    },
                                }}
                            />
                        </div>
                    </Stack>
                </Col>
                <Col>
                    <Stack gap={3}>
                        <div className="form-input">
                            <Form.Label>Ngày Bắt đầu</Form.Label>
                            <Form.Control required type="date" onChange={updateStartDate}/>
                        </div>
                        <div className="form-input">
                            <Form.Label>Ngày Kết thúc</Form.Label>
                            <Form.Control required type="date" onChange={updateEndDate}/>
                        </div>
                        <div className="form-input">
                            <Form.Label>Choose file</Form.Label>
                            <Form.Control type="file" required  onChange={handleFileInputChange} />
                        </div>
                        <div className="form-input">
                            <Form.Label>Select separation symbol</Form.Label>
                            <Form.Select required onChange={handleSeparationSymbolChange}>
                                {separationSymbols.map(type => <option>{type}</option>)}
                            </Form.Select>
                        </div>
                    </Stack>
                </Col>
            </Row>  
        <div class="container">
            <div className="row">
                <div className="col text-end"><button type="button" class="btn btn-warning" onClick={refreshPage}>Nhập Lại</button></div>
                {/* Tại bước này tạo một onclick => Khi bấm vào sẽ add tên các file vào một list mới để bắt đầu phân tích  */}
                <div className="col"><button type="button" class="btn btn-primary">Thực Hiện</button></div>
            </div>
        </div>
    </div>
    <div className='tables-grid'>
        <Row>
            <Col>
                <Table striped bordered>
                    <tbody>
                        <tr>
                            <td className='table-title' colSpan={2}>Thống kê bảng tốt / cần kiểm tra</td>
                        </tr>
                        <tr>
                            <td><Pie data={dataForPie}/></td>
                        </tr>
                        
                    </tbody>
                </Table>
            </Col>
            <Col>
            <Table striped bordered>
                {
                    setOfDataInBar.map(dataInBar => 
                    <tbody>
                        <tr>
                            <td className='table-title' colSpan={2}>Biểu đồ Cột: {dataInBar.fileName}</td>
                        </tr>
                        {/* Component rieng voi props la set of Data! */}
                        <tr>
                            <td colSpan={2}><Bar data={dataForBarChart(dataInBar)} /></td>
                        </tr>
                        
                        <tr>
                            <td>Text</td>
                            <td>{dataInBar.text}</td>
                        </tr>

                        <tr>
                            <td>Numeric</td>
                            <td>{dataInBar.numeric}</td>
                        </tr>

                        <tr>
                            <td>DateTime</td>
                            <td>{dataInBar.datetime}</td>
                        </tr>

                        <tr>
                            <td>Number of Lines</td>
                            <td>{dataInBar.numberOfLines}</td>
                        </tr>
                    </tbody>)
                }
                </Table>
            </Col>
        </Row>
    </div>    
    
    <div className='tables-grid'>
        <Row>            
            <Table striped bordered>
                    <tbody className="text-center">
                        <tr>
                            <td className='table-title' colSpan={4}>Thống kê Thông tin Bảng Dữ liệu</td>
                        </tr>
                        <tr>
                            <th>STT</th>
                            <th>Cơ sở Dữ liệu</th>
                            <th>Tên Bảng</th>
                            <th>Chất lượng Dữ liệu</th>
                        </tr>

                        {basicInformation.tableCheck.map((table, i) => 
                            <tr>
                            <td>{++i}</td>
                            <td>{basicInformation.nameOfDatabase}</td>
                            <td>{table}</td>
                            {/* Add thuộc tính của từng bảng? */}
                            <td>Tốt</td>
                            </tr> 
                        )}
                    </tbody>

                </Table>
        
                <Table striped bordered>
                    <tbody className="text-center">
                        <tr>
                            <td className='table-title' colSpan={4}>Thống kê Thông tin File Dữ liệu</td>
                        </tr>


                        <tr>
                            <th>STT</th>
                            <th>Tên File</th>
                            <th>Chất lượng Dữ liệu</th>
                        </tr>

                        {setOfDataInBar.map((dataInBar, i) => 
                            <tr>
                            <td>{++i}</td>
                            <td>{dataInBar.fileName}</td>
                            <td>Tốt</td>
                            </tr>
                        )}
                    </tbody>

                </Table>

                <Table striped bordered>
                    <tbody className="text-center">
                        <tr>
                            <td className='table-title' colSpan={6}>Thống kê Thông tin Trường Dữ liệu</td>
                        </tr>
                        <tr>
                            <th>STT</th>
                            <th>Tên File</th>
                            <th>Text</th>
                            <th>Numeric</th>
                            <th>Date</th>
                            <th>Số dòng</th>
                        </tr>

                        {
                            setOfDataInBar.map((dataInBar,i) =>
                                <tr>
                                <td>{++i}</td>
                                <td>{dataInBar.fileName}</td>
                                <td>{dataInBar.text}</td>
                                <td>{dataInBar.numeric}</td>
                                <td>{dataInBar.datetime}</td>
                                <td>{dataInBar.numberOfLines}</td>
                                </tr>    
                            )
                        }
                        
                    </tbody>

                </Table>
            </Row>
    </div>   

      </>
    );
}