# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone, timedelta
import os

from functools import wraps

from flask import request, jsonify, make_response
from flask_restx import Api, Resource, fields

import jwt

from .models import db, Users, Upload, JWTTokenBlocklist
from .config import BaseConfig

from .service.getDataService import get_dashboard_lcr_nsfr_data, get_dashboard_bar_charts_data, get_lcr_data
from .service.uploadDataService import get_table_list

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
                    "msg": "Email already taken"}, 400

        new_user = Users(username=_username, email=_email, password=_password, roles=["admin"])
        new_user.save()

        return {"success": True,
                "userID": new_user.id,
                "msg": "The user was successfully registered"}, 200


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
                    "msg": "This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Wrong credentials."}, 400

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
        print("con cancjanckjasdnfjkn")
        _jwt_token = request.cookies.get('jwtToken')

        jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
        jwt_block.save()

        current_user.set_jwt_auth_active(False)
        current_user.save()

        response = make_response(jsonify({"success": True}))
        response.delete_cookie('jwtToken')
        return response    

@rest_api.route('/upload')
class UploadResource(Resource):
    @token_required(required_roles=["editor"])
    def post(current_user, self):
        username = current_user.username
        uploaded_file = request.files.get('file')
        expected_file_type = request.form.get('fileType')  # Get the expected fileType from the request data
        table_name = request.form.get('tableName')

        user = Users.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 401
        
       # Get the file extension from the uploaded file's filename
        file_extension = uploaded_file.filename.rsplit('.', 1)[-1]
        
        # Validate the expected file type based on file extension
        if (expected_file_type == 'csv' and file_extension == 'csv') or \
           (expected_file_type == 'xlsx' and file_extension == 'xlsx') or \
           (expected_file_type == 'xls' and file_extension == 'xls'):
            # Handle CSV, Excel (xlsx), and Excel (xls) files
            file_name = f"{table_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"

            # save file to resource
            resource_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data_files')
            full_file_path = os.path.join(resource_folder, file_name)
            uploaded_file.stream.seek(0)  # Reset the stream position
            uploaded_file.save(full_file_path)
            
            upload = Upload(user_id=user.id, filename=file_name)
            db.session.add(upload)
            db.session.commit()
            
            return {"message": "File được tải lên thành công"}
        else:
            return {"error": "Invalid file format or mismatched fileType"}, 400
        

@rest_api.route('/upload/history')
class UploadHistoryResource(Resource):
    @token_required(required_roles=['viewer'])
    def get(current_user, self):
        username = "m1"
        
        user = Users.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 401
                
        uploads = Upload.query.filter_by(user_id=user.id).all()
        upload_history = [{"filename": upload.filename, "upload_time": upload.upload_time.isoformat()} for upload in uploads]
        
        return {"upload_history": upload_history}
    
@rest_api.route('/upload/getTableList', methods=['GET'])
class GetDashboardBarChartsData(Resource):
    @token_required(required_roles=['viewer'])
    def get(current_user, self):
        data = get_table_list()
        return jsonify(data)  
    

# @rest_api.route('/data/getDashboardLcrNsfr')
# class GetDashboardData(Resource):
#     @token_required(required_roles=['viewer'])
#     def get(current_user, self):
#         date = request.args.get('date')
#         print(date)
#         data = get_dashboard_lcr_nsfr_data(date)

#         return jsonify(data)
        

@rest_api.route('/data/getDashboardLcrNsfr', methods=['POST'])
class GetDashboardData(Resource):
    @token_required(required_roles=['viewer'])
    def post(current_user, self):
        request_data = request.get_json()
        requested_date = request_data.get('date')  # Extract the date from the request data

        data = get_dashboard_lcr_nsfr_data(requested_date)

        return jsonify(data) 
    

@rest_api.route('/data/getDashboardBarCharts', methods=['GET'])
class GetDashboardBarChartsData(Resource):
    @token_required(required_roles=['viewer'])
    def get(current_user, self):
        data = get_dashboard_bar_charts_data()
        return jsonify(data)  
    

@rest_api.route('/data/getLcr', methods=['GET'])
class GetLcr(Resource):
    def get(self):
        lcr_data = get_lcr_data(0)
        return lcr_data