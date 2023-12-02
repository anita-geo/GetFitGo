from flask import Blueprint, jsonify, request
from db import get_db

app_login = Blueprint('app_login',__name__)

@app_login.route('/login', methods=['POST'])
def get_login_detail():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        _result = -1

        if _username.strip() == "":
            return "Username is empty", 400

        if _password.strip() == "":
            return "Password is empty", 400

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('CheckCredentials',(_username, _password, _result))
        cur.execute("SELECT @_CheckCredentials_2")
        _result = cur.fetchone()[0]

        if _result == 1:
            return "Successfully logged in"
        else:
            return "Username and passowrd is invalid", 401
            
    except KeyError:
        return "Username and passowrd is invalid", 401
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()