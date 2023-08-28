import { Modal, Button, Stack, Form } from 'react-bootstrap';
import { useState } from "react";

import './chooseFileDateDialog.css'


export default function ChooseFileDateDialog({
    reportingDate,
    onCloseHandle, 
    extraTables=[],
    onSubmitHandle,
}) {

    const convertDictToArray = () => {
        return Object.keys(extraTables).map(tableName => {
            return {
              tableName: tableName,
              closest_versions: extraTables[tableName],
              choosen_version: extraTables[tableName].length > 0 ? extraTables[tableName][0] : "",
            };
        });
    } 

    const convertTableArrayToDict = (tableArray) => {
        const dict = {}
        for (const table of tableArray) {
            dict[table.tableName] = table.choosen_version
        }
        return dict
    }

    const [message, setMessage] = useState("Ngày đã chọn không có đủ các bảng yêu cầu. Vui lòng chọn 1 trong 3 phương thức sau: 1.Chọn ngày khác 2.Tải bảng lên trong phần Nhập Dữ liệu 3.Chọn 1 trong các bảng dưới đây để tính toán")
    const [missingTables, setMissingTables] = useState(convertDictToArray(extraTables))
    const handleDateChange = (index, newDate) => {
        const newMissingTables = [...missingTables];
        newMissingTables[index].choosen_version = newDate
        setMissingTables(newMissingTables)
    };

    return (
        <Modal show={true}>
        <Modal.Header>
            <Modal.Title>Kiểm tra dữ liệu</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <Stack gap={1}>
                <b>Ngày báo cáo: {reportingDate} </b>
                <p>{message}</p>
                <b>Các bảng còn thiếu </b>
                {missingTables.map((table, index) => (
                    <div className="form-input">
                        <Form.Label><b>{table.tableName}</b></Form.Label>
                        <Form.Select required onChange={(event) => handleDateChange(index, String(event.target.value))}>
                            {table.closest_versions.map(version => <option>{version}</option>)}
                        </Form.Select>
                    </div>
                ))}
            </Stack>
        </Modal.Body>
        <Modal.Footer>
            <Button variant="primary" onClick={() => 
                {   
                    onSubmitHandle({
                        "reportingDate":reportingDate,
                        "extraTables": convertTableArrayToDict(missingTables)
                    })
                }
            }>
                Tính toán lại
            </Button>
            <Button variant="secondary" onClick={onCloseHandle}>
                Đóng
            </Button>
        </Modal.Footer>
        </Modal>
    )
}
