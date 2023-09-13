# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone, timedelta
import os
import pandas as pd

from functools import wraps

from flask import request, jsonify, make_response
from flask_restx import Api, Resource, fields

import jwt

from .models import db, Users, Upload, JWTTokenBlocklist, CalculatedData
from .config import BaseConfig

from .service.getDataService import get_dashboard_lcr_nsfr_data, calculate_lcr, calculate_nsfr
from .service import getDataService

from .tableNames import TABLES, MAPPING_TABLES, OTHER_TABLES, REGULATORY_TABLES

import json

rest_api = Api(version="1.0", title="Users API")


"""
    Flask-Restx models for api request and response data
"""

signup_model = rest_api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                              "email": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=4, max_length=16)
                                              })

login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                            "password": fields.String(required=True, min_length=4, max_length=16)
                                            })

user_edit_model = rest_api.model('UserEditModel', {"userID": fields.String(required=True, min_length=1, max_length=32),
                                                   "username": fields.String(required=True, min_length=2, max_length=32),
                                                   "email": fields.String(required=True, min_length=4, max_length=64)
                                                   })


"""
    Helper function for roles check
"""
def roles_check(user_roles, required_roles):
    if "admin" in user_roles:
        user_roles.append("viewer")
        user_roles.append("editor")
    for required_role in required_roles:
        if required_role not in user_roles:
            return False
    return True    

"""
   Helper function for JWT token required
"""

def token_required(required_roles=[]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('jwtToken')

            if not token:
                return {"success": False, "msg": "Valid JWT token is missing"}, 401

            try:
                data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
                current_user = Users.get_by_email(data["email"])

                if not current_user:
                    return {"success": False, "msg": "Sorry. Wrong auth token. This user does not exist."}, 401

                token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()
                if token_expired is not None:
                    return {"success": False, "msg": "Token revoked."}, 401

                if not current_user.check_jwt_auth_active():
                    return {"success": False, "msg": "Token expired."}, 401

                # Check roles here
                user_roles = current_user.get_roles()
                if not (roles_check(user_roles=user_roles, required_roles=required_roles)):
                    return {"success": False, "msg": "Insufficient permissions"}, 403

            except:
                return {"success": False, "msg": "Token is invalid"}, 401

            return f(current_user, *args, **kwargs)

        return wrapper

    return decorator

"""
    Flask-Restx routes
"""


@rest_api.route('/api/users/register')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False,
                    "msg": "Email đã được sử dụng"}, 400

        new_user = Users(username=_username, email=_email, password=_password, roles=["admin"])
        token = jwt.encode({'email': _email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)

        new_user.set_jwt_auth_active(True)
        new_user.save()

        response = make_response(jsonify({"success": True,
                "token": token,
                "user": new_user.toJSON(),
                }))
        response.set_cookie('jwtToken', token, httponly=True)
        return response

@rest_api.route('/api/users/login')
class Login(Resource):
    """
       Login user by taking 'login_model' input and return JWT token
    """

    @rest_api.expect(login_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)

        if not user_exists:
            return {"success": False,
                    "msg": "Email không tồn tại"}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Sai tên đăng nhập hoặc mật khẩu"}, 400

        # create access token uwing JWT
        token = jwt.encode({'email': _email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)

        user_exists.set_jwt_auth_active(True)
        user_exists.save()

        response = make_response(jsonify({"success": True,
                "token": token,
                "user": user_exists.toJSON(),
                }))
        response.set_cookie('jwtToken', token, httponly=True)
        return response

@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's username or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @token_required
    def post(current_user, self):
        req_data = request.get_json()

        _new_username = req_data.get("username")
        _new_email = req_data.get("email")

        if _new_username:
            current_user.update_username(_new_username)

        if _new_email:
            current_user.update_email(_new_email)

        self.save()

        return {"success": True}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Logs out User using 'logout_model' input
    """
    @token_required(required_roles=[])
    def post(current_user, self):
        _jwt_token = request.cookies.get('jwtToken')

        jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
        jwt_block.save()

        current_user.set_jwt_auth_active(False)
        current_user.save()

        response = make_response(jsonify({"success": True}))
        response.delete_cookie('jwtToken')
        return response    

"""
    Tải 1 file dữ liệu lên hệ thống. Đối với các file không phải Mapping hoặc Regulatory, tên 
    của file bao gồm thêm ngày update để sử dụng cho code tính toán
    Database ghi lại lịch sử upload 

    - username: dùng để lưu vào lịch sử upload
    - uploaded_file: file dữ liệu 
    - fileTyle: phần lớn là csv
    - tableName: file dữ liệu tương ứng với bảng nào
    - uploaded_date: file dữ liệu này là của ngày nào 
"""
@rest_api.route('/upload')
class UploadResource(Resource):
    @token_required(required_roles=["editor"])
    def post(current_user, self):
        username = current_user.username
        uploaded_file = request.files.get('file')
        expected_file_type = request.form.get('fileType')  # Get the expected fileType from the request data
        table_name = request.form.get('tableName')
        uploaded_date = datetime.strptime(request.form.get('uploadDate'), '%Y-%m-%d')
        converted_uploaded_time = uploaded_date.strftime('%d-%m-%Y')
 
        user = Users.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 401
        
       # Get the file extension from the uploaded file's filename
        file_extension = uploaded_file.filename.rsplit('.', 1)[-1]
        # existing_upload = Upload.query.filter_by(filename=table_name, upload_time=uploaded_date).first()
        # Validate the expected file type based on file extension
        if (expected_file_type == 'csv' and file_extension == 'csv') or \
           (expected_file_type == 'xlsx' and file_extension == 'xlsx') or \
           (expected_file_type == 'xls' and file_extension == 'xls'):
            # save file to resource
            # resource_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data_files')
            if table_name in TABLES:
                file_name = f"{table_name}_{converted_uploaded_time}.{file_extension}"
                path_to_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service', 'Main_V2_final', 'Main_V2_final', TABLES[table_name], file_name)
            elif table_name in MAPPING_TABLES:
                file_name = f"{table_name}.{file_extension}"
                path_to_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service', 'Main_V2_final', 'Main_V2_final', MAPPING_TABLES[table_name], file_name)
            elif table_name in REGULATORY_TABLES:
                file_name = f"{table_name}.{file_extension}"
                path_to_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service', 'Main_V2_final', 'Main_V2_final', REGULATORY_TABLES[table_name], file_name)
            else:
                return {"error": f"Không tìm được bảng nào với tên {table_name}"}, 400 

            uploaded_file.stream.seek(0)  # Reset the stream position
            uploaded_file.save(path_to_file)
            
            # only do this if the file has not been uploaded in the same day 
            existing_upload = Upload.query.filter_by(filename=table_name, upload_time=uploaded_date).first()
            if existing_upload is None:
                upload = Upload(user_id=user.id, filename=table_name, upload_time=uploaded_date)
                db.session.add(upload)
                db.session.commit()
            
            return {"message": "File được tải lên thành công"}
        else:
            return {"error": "Invalid file format or mismatched fileType"}, 400
        

"""
    Lấy lần gần nhất upload của tất cả các file dữ liệu 
"""
@rest_api.route('/upload/history')
class UploadHistoryResource(Resource):
    @token_required(required_roles=['viewer'])
    def get(current_user, self):
        files_latest_upload_dates = []

        for tablename in list(TABLES.keys()):
            latest_upload = Upload.query.filter_by(filename=tablename).order_by(Upload.upload_time.desc()).first()
            if latest_upload:
                files_latest_upload_dates.append({'filename':latest_upload.filename, 'upload_time': latest_upload.upload_time.strftime("%Y-%m-%d")})
        return {"upload_history": files_latest_upload_dates}


"""
    Lấy danh sách các bảng dữ liệu 
"""
@rest_api.route('/upload/getTableList', methods=['GET'])
class GetDashboardBarChartsData(Resource):
    @token_required(required_roles=['viewer'])
    def get(current_user, self):
        return jsonify(list(TABLES.keys()))
    
    
"""
    Tính toán cho Bảng chung. Người dùng cần cung cấp 1 ngày cụ thể. Nếu trong ngày này không có đủ file dữ liệu
    cần thiêt cho tính toán, thông báo lại cho người dùng còn thiếu những file nào

    Người dùng có thể chọn ngày cụ thể cho từng file trong trường hợp ngày đã chọn không có đủ file. Các thông tin 
    này được lưu trong extraTables. Đối với các bảng còn lại, sử dụng reportingDate để tìm file tính toán

    Sau khi tính toán thành công, lưu lại kết quả vào database. Kết quả được lưu lấy thời gian theo reportingDate

    - reportingDate: chọn ngày tính toán để tìm các file tương ứng
    - extraTables: cho phép người dùng chọn file tính toán khác ngày với reportingDate 
"""
@rest_api.route('/data/calculateDashboardLcrNsfr', methods=['POST'])
class CalculateDashboardData(Resource):
    def post(self):
        data = request.get_json()
        reporting_date = data.get("reportingDate")
        extra_tables_request = data.get("extraTables")
        if not reporting_date:
            return {"message": "Reporting date is missing in the request."}, 400

        extra_tables_needed = checkTables(extra_tables_request, reporting_date)
        if (len(extra_tables_needed) > 0):
            return jsonify({
                "success":False,
                "extraTables":extra_tables_needed,
                "data":{}
        })
        converted_date = datetime.strptime(reporting_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        data['reportingDate'] = converted_date
        for key, value in extra_tables_request.items():
            extra_tables_request[key] = datetime.strptime(value, '%Y-%m-%d').strftime('%d-%m-%Y')

        result = get_dashboard_lcr_nsfr_data(data)

        return jsonify({
            "success":True,
            "extraTables": {},
            "data": result
        })    


"""
    Tính toán cho Bảng LCR. Người dùng cần cung cấp 1 ngày cụ thể. Nếu trong ngày này không có đủ file dữ liệu
    cần thiêt cho tính toán, thông báo lại cho người dùng còn thiếu những file nào

    Người dùng có thể chọn ngày cụ thể cho từng file trong trường hợp ngày đã chọn không có đủ file. Các thông tin 
    này được lưu trong extraTables. Đối với các bảng còn lại, sử dụng reportingDate để tìm file tính toán

    Sau khi tính toán thành công, lưu lại kết quả vào database. Kết quả được lưu lấy thời gian theo reportingDate

    - reportingDate: chọn ngày tính toán để tìm các file tương ứng
    - extraTables: cho phép người dùng chọn file tính toán khác ngày với reportingDate 
"""
@rest_api.route('/data/calculateLcr', methods=['POST'])
class CalculateLcr(Resource):
    def post(current_user):
        data = request.get_json()
        reporting_date = data.get("reportingDate")
        converted_date = datetime.strptime(reporting_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        extra_tables_request = data.get("extraTables")
        if not reporting_date:
            return {"message": "Reporting date is missing in the request."}, 400

        extra_tables_needed = checkTables(extra_tables_request, reporting_date)
        if (len(extra_tables_needed) > 0):
            return jsonify({
                "success":False,
                "extraTables":extra_tables_needed,
                "data":{}
        })

        data['reportingDate'] = converted_date
        for key, value in extra_tables_request.items():
            extra_tables_request[key] = datetime.strptime(value, '%Y-%m-%d').strftime('%d-%m-%Y')

        lcr_data = calculate_lcr(data)

        return jsonify({
            "success":True,
            "extraTables": {},
            "data": lcr_data
        })


"""
    Tính toán cho Bảng NSFR. Người dùng cần cung cấp 1 ngày cụ thể. Nếu trong ngày này không có đủ file dữ liệu
    cần thiêt cho tính toán, thông báo lại cho người dùng còn thiếu những file nào

    Người dùng có thể chọn ngày cụ thể cho từng file trong trường hợp ngày đã chọn không có đủ file. Các thông tin 
    này được lưu trong extraTables. Đối với các bảng còn lại, sử dụng reportingDate để tìm file tính toán

    Sau khi tính toán thành công, lưu lại kết quả vào database. Kết quả được lưu lấy thời gian theo reportingDate

    - reportingDate: chọn ngày tính toán để tìm các file tương ứng
    - extraTables: cho phép người dùng chọn file tính toán khác ngày với reportingDate 
"""
@rest_api.route('/data/calculateNsfr', methods=['POST'])
class CalculateNfsr(Resource):
    def post(current_user):
        data = request.get_json()
        reporting_date = data.get("reportingDate")
        extra_tables_request = data.get("extraTables")
        if not reporting_date:
            return {"message": "Reporting date is missing in the request."}, 400

        extra_tables_needed = checkTables(extra_tables_request, reporting_date)
        if (len(extra_tables_needed) > 0):
            return jsonify({
                "success":False,
                "extraTables":extra_tables_needed,
                "data":{}
        })
    
        # request_data = request.get_json()
        # requested_date = request_data.get('reportingDate')  # Extract the date from the request data
        converted_date = datetime.strptime(reporting_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        data['reportingDate'] = converted_date
        for key, value in extra_tables_request.items():
            extra_tables_request[key] = datetime.strptime(value, '%Y-%m-%d').strftime('%d-%m-%Y')
        
        nsfr_data = calculate_nsfr(data)

        return jsonify({
            "success":True,
            "extraTables": {},
            "data": nsfr_data
        })
    

"""
    Lấy dữ liệu được lưu trữ của 1 chỉ số cho 1 ngày cụ thể

    - fieldName: tên chỉ số
    - reportingDate: ngày được chọn
"""
@rest_api.route('/data/getCalculatedData', methods=['POST'])
class GetCalculatedData(Resource):
    def post(current_user):
        data = request.get_json()
        reporting_date = data.get("reportingDate")
        converted_date = datetime.strptime(reporting_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        field_name = data.get("fieldName")

        calculated_data = CalculatedData.query.filter_by(date=converted_date, field_name=field_name).first()

        if calculated_data:
            # Data exists in the database, return it
            return jsonify({
                "success": True,
                "data": json.loads(calculated_data.value)
            })
        else:
            return jsonify({
                "success": False,
                "data": {},
                "error": f"Không có dữ liệu nào được lưu cho ngày {converted_date}. Vui lòng chạy tính toán"
            })
        
"""
    Lấy dữ liệu được lưu trữ của 1 chỉ số cho trong 1 thời gian cụ thể. Các khoảng thời gian được hỗ trợ
    bao gồm:
        + n ngày trước: representing values của n ngày gần nhất
        + n tuần trước: Ví dụ với ngày 30/08/2023, đặt number_of_data_point = 4
        sẽ trả về dữ liệu của 4 ngày sau: 30/08, 23/08. 16/08, 09/08
        + n tháng trước: trả về dữ liệu của ngày đầu tiên trong tháng của n tháng trước. Ví dụ với ngày 30/08/2023, 
        đặt number_of_data_point = 4 sẽ trả về dữ liệu của 4 ngày sau: 01/08, 01/07. 01/06, 01/05

    - fieldName: tên chỉ số
    - number_of_data_point: số lượng điểm dữ liệu
    - duration: tính theo ngày/tuần/tháng
    """
@rest_api.route('/data/getCalculatedDataByRange', methods=['POST'])
class GetCalculatedDataByRange(Resource):
    def post(self):
        
            data = request.get_json()

            field_name = data['fieldName']
            number_of_data_point = data['numberOfDataPoint']
            duration = data['duration']

            converted_date = datetime.now().date().strftime('%d-%m-%Y')

            date_list = []
            if duration == "days":
                date_list = getDataService.get_last_days(converted_date, number_of_data_point)
            elif duration == "weeks":
                date_list = getDataService.get_last_weeks(converted_date, number_of_data_point)
            elif duration == "months":
                date_list = getDataService.get_first_date_of_last_months(converted_date, number_of_data_point)

            # Initialize the result list
            result = []

            # Loop through the date list and fetch values for each date
            for date in date_list:
                # Query the database for the value on the given date and fieldName
                query_result = CalculatedData.query.filter_by(date=date, field_name=field_name).first()

                # If no data found, append 0; otherwise, append the value
                if query_result:
                    if (query_result.value == ""):
                        result.append(0)
                    else:
                        result.append(json.loads(query_result.value))
                else:
                    result.append(0)

            return jsonify({"success": True, 
                            "data": result,
                            "dateList": date_list
                            })


"""
    Lấy danh sách các bảng Mapping và Regulatory
"""
@rest_api.route('/data/getNonDataTableList', methods=['GET'])
class GetNonDatatableList(Resource):
    def get(self):
        return {
            "mapping_tables": list(MAPPING_TABLES.keys()),
            "regulatory_tables": list(REGULATORY_TABLES.keys()),
            "other_tables": list(OTHER_TABLES.keys())
        }
    

"""
    Lấy dữ liệu hiện có của 1 bảng Mapping hoặc Regulatory 
"""    
@rest_api.route('/data/getNonDataTable', methods=['GET'])
class GetNonDatatableList(Resource):
    def get(self):
        table_name = request.args.get('table_name')
        if not table_name:
            return jsonify({"error": "Table name is missing in the request."}), 400

        # Define a dictionary that combines all tables and their paths
        all_tables = {**MAPPING_TABLES, **REGULATORY_TABLES, **OTHER_TABLES}

        # Check if the requested table exists in the dictionary
        if table_name in all_tables:
            # table_path = os.path.join(all_tables[table_name])
            table_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service', 'Main_V2_final', 'Main_V2_final', all_tables[table_name], f'{table_name}.csv')
            # Check if the file exists
            if os.path.exists(table_path):
                # Read the CSV file using pandas
                df = pd.read_csv(table_path)
                
                # Convert the DataFrame to a JSON object
                table_data = df.to_json(orient='split')
                
                # Return the JSON response
                return jsonify(table_data)
            else:
                return jsonify({"error": "Không tìm thấy bảng."}), 401
        else:
            return jsonify({"error": "Không tìm thấy bảng."}), 401
        

"""
    Xem bản mẫu dữ liệu của 1 bảng. 
"""        
@rest_api.route('/data/getPreviewDataTable', methods=['GET'])
class GetPreviewDataTable(Resource):
    def get(self):
        table_name = request.args.get('table_name')
        if not table_name:
            return jsonify({"error": "Table name is missing in the request."}), 400

        # Check if the requested table exists in the dictionary
        if table_name in TABLES:
            # table_path = os.path.join(all_tables[table_name])
            table_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service', 'Main_V2_final', 'Main_V2_final', TABLES[table_name], f'{table_name}_preview.csv')
            # Check if the file exists
            if os.path.exists(table_path):
                # Read the CSV file using pandas
                df = pd.read_csv(table_path)
                
                # Convert the DataFrame to a JSON object
                table_data = df.to_json(orient='split')
                
                # Return the JSON response
                return jsonify(table_data)
            else:
                return jsonify({"error": "Table not found."}), 401
        else:
            return jsonify({"error": "Table not found."}), 401

def checkTables(extra_tables_request, reporting_date):
    # extra_tables_request is a dictionary with name of table and date

    requested_date = datetime.strptime(reporting_date, '%Y-%m-%d').date()
    extra_table_needed = {}

    for tablename in list(TABLES.keys()):
        # check for each table
        if tablename in extra_tables_request:
            extra_requested_date =  datetime.strptime(extra_tables_request[tablename], '%Y-%m-%d').date()
            uploads_on_date = Upload.query.filter(
                Upload.filename == tablename,
                Upload.upload_time >= datetime.combine(extra_requested_date, datetime.min.time()),
                Upload.upload_time < datetime.combine(extra_requested_date+ timedelta(days=1), datetime.min.time())
            ).order_by(Upload.upload_time.desc()).limit(1).all()
        else:
            uploads_on_date = Upload.query.filter(
                Upload.filename == tablename,
                Upload.upload_time >= datetime.combine(requested_date, datetime.min.time()),
                Upload.upload_time < datetime.combine(requested_date + timedelta(days=1), datetime.min.time())
            ).order_by(Upload.upload_time.desc()).limit(1).all()

        if not uploads_on_date:
            # If no uploads on the requested date, find closest versions
            closest_versions = Upload.query.filter(
                Upload.filename == tablename,
                Upload.upload_time <= requested_date
            ).order_by(Upload.upload_time.desc()).limit(5).all()
            closest_dates = [upload.upload_time.strftime("%Y-%m-%d") for upload in closest_versions]
            extra_table_needed[tablename] = closest_dates

    return extra_table_needed