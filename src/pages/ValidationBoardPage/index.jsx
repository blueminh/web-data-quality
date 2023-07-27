import {React, useState} from "react";
import {Form, Row, Col, Table} from 'react-bootstrap';
import './ValidationPage.css';

export default function ValidationPage() {
    const [fileNames, setFileNames] = useState([]);

   const handleFileChange = (event) => {
        const files = event.target.files;
        console.log(files)
        setFileNames(Array.from(files).map(extractFileName => extractFileName.name))
      }

    return (
        <>
<div class="container text-center" style={{marginTop:"20px"}}>
  <div class="row">
    <div class="col">
    <h3>Cơ sở Dữ liệu</h3>
    </div>
    <div class="col">
    <h3>KPMG</h3>
    </div>
  </div>
      <Row style={{marginTop:"20px"}}>
        <Col><h5>Ngày Dữ liệu</h5></Col>
        <Col><strong>Bắt đầu:</strong> xxxx-xx-xx -> <strong>Kết thúc:</strong> xxxx-xx-xx</Col>
      </Row>
    <div class="row">
    <div class="col">
      <h5>Tên bảng cần kiểm tra:</h5> 
    </div>
    <div class="col">
      -Placeholder-
    </div>
  </div>
  <div class="row">
  <div class="col">
      <h5>Tên bảng loại trừ:</h5> 
    </div>
    <div class="col">
        -Placeholder-
    </div>
    </div>
</div>
<div>
<div class="container text-center" style={{marginTop: "20px"}}>
<input className = "text-center" type="file" onChange={handleFileChange} multiple />
</div>
<div className='tables-grid'>
                <Row>
                <Col>
                    <Table striped bordered>
                            <tbody>
                                <tr>
                                    <td className='table-title' colSpan={2}>Tên File Để Upload</td>
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
        <div className="col text-end"><button type="button" class="btn btn-warning">Nhập Lại</button></div>
        <div className="col"><button type="button" class="btn btn-primary">Thực Hiện</button></div>
        </div>
</div>
</div>

      </>
    );
}