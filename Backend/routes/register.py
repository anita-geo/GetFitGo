from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

app_register = Blueprint('app_register',__name__)

@app_register.route('/register-trainer', methods=['POST'])
def register_trainer():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        _email = _json['email']

        _firstName = _json.get('firstName', None)
        _lastName = _json.get('lastName', None)
        _gender = _json.get('gender', None)
        _state = _json.get('state', None)
        _city = _json.get('city', None)
        _mobileNumber = _json.get('mobileNumber', None)
        _aboutMe = _json.get('aboutMe', None)

        if _username.strip() == "":
            return "Username is empty", 400

        if _password.strip() == "":
            return "Password is empty", 400
        
        if _email.strip() == "":
            return "Email is empty", 400
        
        if _firstName.strip() == "":
            return "First name is empty", 400

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('CreateUser',(_username, _email, _password))
        
        # The create user was successful
        if cur.rowcount > 0:
            cur.callproc('InsertOrUpdateTrainer',(_firstName, _lastName, _gender, _state, _city, _mobileNumber, _email, _aboutMe))
            if cur.rowcount > 0:
                return "Trainer created successfully"
            else:
                return "Failed to create trainer", 500
        else:
            return "Failed to create user", 500
    except pymysql.MySQLError as e:
        connection.rollback()
        if len(e.args) > 1:
            return e.args[1], 500
        return 'Something went wrong', 500
    except Exception as e:
        connection.rollback()
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_register.route('/register-client', methods=['POST'])
def register_client():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        _email = _json['email']

        _firstName = _json.get('firstName', None)
        _lastName = _json.get('lastName', None)
        _gender = _json.get('gender', None)
        _streetNo = _json.get('streetNo', None)
        _streetName = _json.get('streetName', None)
        _city = _json.get('city', None)
        _state = _json.get('state', None)
        _mobileNumber = _json.get('mobileNumber', None)

        _height = _json.get('height', None)
        _weight = _json.get('height', None)
        _bodyType = _json.get('bodyType', None)

        if (_weight is not None and _height is not None):
            _bmi = (_weight) / ((_height/100) * (_height/100))
        else:
            _bmi = None
        
        _targetWeight = _json.get('height', None)
        _level = _json.get('height', None)
        _aboutMe = _json.get('aboutMe', None)

        if _username.strip() == "":
            return "Username is empty", 400

        if _password.strip() == "":
            return "Password is empty", 400
        
        if _email.strip() == "":
            return "Email is empty", 400
        
        if _firstName.strip() == "":
            return "First name is empty", 400

        connection = get_db()
        cur = connection.cursor()
        connection.begin()
        cur.callproc('CreateUser',(_username, _email, _password))
        
        # The create user was successful
        if cur.rowcount > 0:
            cur.callproc('InsertUserInfo',(_email, _firstName, _lastName, _gender,_streetNo,_streetName,_city,  _state, _mobileNumber, _height, _weight,_bodyType, _bmi,_targetWeight, _level, _aboutMe))
            if cur.rowcount > 0:
                return "Client created successfully"
            else:
                return "Failed to create client", 500
        else:
            return "Failed to create user", 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()