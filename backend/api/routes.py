# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import request, jsonify, make_response
from flask_restx import Api, Resource, fields

import jwt
import magic

from .models import db, Users, Upload, JWTTokenBlocklist
from .config import BaseConfig
import requests

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
   Helper function for JWT token required
"""

def token_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.cookies.get('jwtToken')

        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 401

        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])

            if not current_user:
                return {"success": False,
                        "msg": "Sorry. Wrong auth token. This user does not exist."}, 403

            token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()

            if token_expired is not None:
                return {"success": False, "msg": "Token revoked."}, 403

            if not current_user.check_jwt_auth_active():
                return {"success": False, "msg": "Token expired."}, 403

        except:
            return {"success": False, "msg": "Token is invalid"}, 403

        return f(current_user, *args, **kwargs)

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

        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
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
                "user": user_exists.toJSON()}))
        response.set_cookie('jwtToken', token, httponly=True)
        return response

@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's username or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @token_required
    def post(self, current_user):

        req_data = request.get_json()

        _new_username = req_data.get("username")
        _new_email = req_data.get("email")

        if _new_username:
            self.update_username(_new_username)

        if _new_email:
            self.update_email(_new_email)

        self.save()

        return {"success": True}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Logs out User using 'logout_model' input
    """

    @token_required
    def post(self, current_user):

        _jwt_token = request.cookies.get('jwtToken')

        jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
        jwt_block.save()

        self.set_jwt_auth_active(False)
        self.save()

        response = make_response(jsonify({"success": True}))
        response.delete_cookie('jwtToken')
        return response
    

@rest_api.route('/upload')
class UploadResource(Resource):
    @token_required
    def post(self, current_user):
        username = request.form.get('username')
        uploaded_file = request.files.get('file')
        expected_file_type = request.form.get('fileType')  # Get the expected fileType from the request data

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
            file_name = f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
            uploaded_file.stream.seek(0)  # Reset the stream position
            uploaded_file.save(file_name)
            
            upload = Upload(user_id=user.id, filename=file_name)
            db.session.add(upload)
            db.session.commit()
            
            return {"message": "File uploaded successfully"}
        else:
            return {"error": "Invalid file format or mismatched fileType"}, 400
        

@rest_api.route('/upload/history')
class UploadHistoryResource(Resource):
    @token_required
    def get(self, current_user):
        username = request.args.get('username')
        
        user = Users.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 401
        
        uploads = Upload.query.filter_by(user_id=user.id).all()
        upload_history = [{"filename": upload.filename, "upload_time": upload.upload_time.isoformat()} for upload in uploads]
        
        return {"upload_history": upload_history}