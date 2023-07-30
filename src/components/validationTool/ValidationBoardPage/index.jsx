import {React, useState} from "react";
import {Row, Col, Table, Form} from 'react-bootstrap';

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

    const [fileNames, setFileNames] = useState([]);
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
      }])

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


   const handleFileChange = (event) => {
        const files = event.target.files;
        console.log(files)
        setFileNames(Array.from(files).map(extractFileName => extractFileName.name))
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


    return (
        <>
        <div class="container text-center" style={{marginTop:"20px"}}>
            <div class="row">
                <div class="col text-end">
                <h3>Cơ sở Dữ liệu</h3>
                </div>
                <div class="col text-start">
                <h3>{basicInformation.nameOfDatabase}</h3>
                </div>
            </div>
            <Row style={{marginTop:"20px"}}>
                <Col className="text-end"><h5>Ngày Dữ liệu</h5></Col>
                <Col className="text-start">
                <div className="form-input">
                    <Form.Label>Bắt đầu</Form.Label>
                    <Form.Control required type="date" onChange={updateStartDate}/>
                </div>
                <div className="form-input">
                    <Form.Label>Kết thúc</Form.Label>
                    <Form.Control required type="date" onChange={updateEndDate}/>
                </div>

                </Col>
            </Row>
            <div class="row">
                <div class="col text-end">
                <h5>Tên bảng cần kiểm tra</h5> 
                </div>
            <div class="col text-start">
            {basicInformation.tableCheck.map(x => x).join(', ')}
            </div>
        </div>
            <div class="row">
                <div class="col text-end">
                    <h5>Tên bảng loại trừ:</h5> 
                </div>
                <div class="col text-start">
                    {basicInformation.tableEliminate.map(x => x).join(', ')}
                </div>
            </div>
        </div>
    <div>
<div class="container text-center" style={{marginTop: "20px"}}>
<input class="form-control" type="file" id="formFileMultiple" onChange={handleFileChange} multiple></input>
</div>
<div className='tables-grid'>
                <Row>
                <Col>
                    <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>Tên File Để Thực hiện</td>
                                </tr>
                                    {
                                        fileNames.map(x => <tr><td><span><em>{x}</em></span></td></tr>)
                                    }
                            </tbody>
                        </Table>
                    </Col>
                    <Col>
                        <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>Separate</td>
                                </tr>
                                <tr>
                                    <td>Test; Test 2; Test 3</td>
                                </tr>
                            </tbody>
                        </Table>
                    </Col>

                </Row>
            </div>    
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
                                    <td className='table-title' colSpan={2}>Biểu đồ Tròn</td>
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