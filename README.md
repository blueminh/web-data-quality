# Instructions to run the system
## Backend
The backend is implemented using Flask. The flask server runs on port 8085

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- [Python 3.9+](https://www.python.org/downloads/release/python-390/)
- [pip package manager](https://pypi.org/project/pip/)

### Running the flask server

1. Change to the sub-project directory:

   ```shell
   cd backend/
   ```

2. Create and activate a virtual environment:

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the flask project from the `backend` directory

   ```shell
   python run.py
   ```

##  Frontend

### Description

Implemented using ReactJS.

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- [Node.js]
- [npm package manager]

You can find how to install node.js and npm here: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

### Running the frontend

Open the terminal or command prompt and navigate to the project's root directory:

1. Move to the `/frontend` directory

   ```shell
   cd frontend
   ```

2. Run the following command to install the dependencies:

   ```shell
   npm install
   ```

3. After installing all the required dependencies, run this to start the application:
   ```shell
   npm start
   ```

This Runs the app in the development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes. You may also see any lint errors in the console.

# Description
## Backend
Tất cả code nằm trong folder /api. Tất cả các endpoints được viết trong file routes.py.
### 1. File dữ liệu
Tất cả các file dữ liệu cần thiết cho việc tính toán được lưu trong folder /service/Main_V2_final/Main_V2_final/Input_Files. Các file hiện được lưu trữ ở dạng csv và có phần đuôi là ngày tháng năm được upload lên. Code tính toán sẽ import trực tiếp các file này (dùng thư viện pandas). Lưu ý các file Mapping và Regulatory không có ngày trong tên file. Tên và đường dẫn tới các file dữ liệu được lưu trong tableNames.py.

Các endpoints liên quan:

- /upload: Tải 1 file dữ liệu lên hệ thống. Required inputs: username, file, file_type, table_name, upload_date
- /upload/history: Lấy lịch sử upload các file trong hệ thống.
- /upload/getTableList: Lấy danh sách tên các file dữ liệu
- /data/getNonDataTableList: Lấy danh sách các file Mapping và Regulatory 
- /data/getNonDataTable: Lấy dữ liệu của 1 bảng Mapping hoặc Regulatory
- /data/getPreviewDataTable: Lấy bản xem thử (preview) của 1 bẳng dữ liệu


### 2. Tính toán 

Toán bộ code liên quan tới tính toán được lưu trong folder /service/Main_V2_final/Main_V2_final/LCR hoặc /NSFR. UI hiện đang có 3 bảng dữ liệu chính gồm Bảng chung, Bảng LCR và bảng NSFR tương ừng với 3 file tính toán main_Home.py, LCR/main_LCR.py và NSFR/main_NSFR.py.

Để chạy code tính toán, người dùng cần cung cấp 1 ngày cụ thể. Nếu không có đủ các file cho ngày đó, hệ thống sẽ thông báo người dùng cung cấp 1 ngày khác hoặc sử dụng 1 số file cụ thể từ các ngày lân cận. 

Sau khi tính toán, hệ thống tự động lưu lại các chỉ số (xem model CalculatedData). Mỗi chỉ số có 1 code riêng (xem thêm trong /service/getDataService.py).

Các endpoints liên quan:
- /data/calculateDashboardLcrNsfr: tính toán và lưu trữ dữ liệu cho Bảng chung. 
- /data/calculateLcr: tính toán và lưu trữ dữ liệu cho bảng LCR
- /data/calculateNsfr: tính toán và lưu trữ dữ liệu cho bảng NSFR
- /data/getCalculatedData: lấy dữ liệu tính toán được lưu trữ trong hệ thống của 1 field cho 1 ngày cụ thể 
- /data/getCalculatedDataByRange: lấy dữ liệu tính toán được lưu trữ trong hệ thống của 1 field trong 1 khoảng thời gian nhất địng

### 3.Bảo mật và phân quyền
Người dùng cung cấp username, email và password để đăng ký. Để đăng nhập chỉ cần sử dụng email và password. Hệ thống sử dụng jwt token và http-only cho authorization. Hệ thống đang có 3 quyền: admin, viewer và editor. Admin có đầy đủ quyền của viewer và editor. Hiện tại mỗi người dùng mới đăng ký đều được cấp quyền admin. 


## Frontend
### Cấu trúc chung
UI có 4 page chính: LogIn, Register, Calculaiton Tool và Validation Tool (chưa triển khai). 
Page CalculationTool được chia thành 6 tab nhỏ
### Bảo mật
Sau khi đăng nhập vào hệ thống, backend trả về http-only cookies. LƯU Ý: logic hạn chế người dùng truy cập vào các protected route còn rất hạn chế (hiênj tại chỉ sử dụng local storage, người dùng có thể manipulate để access đuọc các protected page, tuy nhiên backend sẽ không chấp nhận request từ các page này.)
### Calculation Page

