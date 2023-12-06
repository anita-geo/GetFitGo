
from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

app_trainer = Blueprint('app_trainer',__name__)

@app_trainer.route('/view-pending-request', methods=['GET'])
def get_pending_request():
    try:
        _trainerEmail = request.args.get('trainerEmail', None)

        if _trainerEmail.strip() == "":
            return "Trainer email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetTrainingRequestsByTrainerEmail',(_trainerEmail,))
        
        data = cur.fetchall() 
        pending_requests = []
        for request_detail in data:
            pending_request = {
                "clientEmail": request_detail[0],
                "trainerEmail": request_detail[1],
                "requestDate": request_detail[2]
            }
        pending_requests.append(pending_request)
        cur.close()
        return jsonify(pending_requests)
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

@app_trainer.route('/request-trainer', methods=['POST'])
def request_trainer():
    try:
        _json = request.json
        _trainerEmail = _json['trainerEmail']
        _clientEmail = _json['clientEmail']

        if _trainerEmail.strip() == "":
            return "Trainer email is empty", 400

        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('CreateTrainingRequest',(_trainerEmail, _clientEmail,))
        
        # The create training request was successful
        if cur.rowcount > 0:
            return "Created training request"
        else:
            return "Failed to create training request", 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_trainer.route('/handle-pending-request', methods=['POST'])
def handle_pending_request():
    try:
        _json = request.json
        _isAccepted = _json['isAccepted']
        _trainerEmail = _json['trainerEmail']
        _clientEmail = _json['clientEmail']

        if _trainerEmail.strip() == "":
            return "Trainer email is empty", 400

        if _clientEmail.strip() == "":
            return "Client email is empty", 400

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('HandleTrainingRequest',(_trainerEmail, _clientEmail, _isAccepted))
        
        # The handle training request was successful
        if _isAccepted:
            msg = 'Training request was accepted'
        else:
            msg = 'Training request was declined'

        if cur.rowcount > 0:
            return msg
        else:
            return "Failed to create user", 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_trainer.route('/view-trainer', methods=['GET'])
def get_trainer():
    try:
        _trainerEmail = request.args.get('trainerEmail', None)

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('ViewTrainer',(_trainerEmail,))
        
        data = cur.fetchall() 
        trainers = []
        for trainer_detail in data:
            pending_request = {
                "firstName": trainer_detail[0],
                "lastName": trainer_detail[1],
                "gender": trainer_detail[2],
                "state": trainer_detail[3],
                "city": trainer_detail[4],
                "mobileNumber": trainer_detail[5],
                "email": trainer_detail[6],
                "aboutMe": trainer_detail[7]
            }
        trainers.append(pending_request)
        return jsonify(trainers)
        
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_trainer.route('/view-trainer-clients', methods=['GET'])
def get_trainer_clients():
    try:
        _trainerEmail = request.args.get('trainerEmail', None)

        if _trainerEmail.strip() == "":
            return "Trainer email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetClientInfo',(None, _trainerEmail,))
        
        data = cur.fetchall() 
        trainerClients = []
        for detail in data:
            client = {
                "clientEmail": detail[0],
                "firstName": detail[1],
                "lastName": detail[2],
                "gender": detail[3],
                "height": detail[4],
                "weight": detail[5],
                "targetWeight": detail[6],
                "bodyType": detail[7],
                "aboutMe": detail[8],
                "level": detail[9],
                "trainerEmail": detail[10],
            }
        trainerClients.append(client)
        return jsonify(trainerClients)
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_trainer.route('/update-trainer', methods=['POST'])
def update_trainer():
    try:
        _json = request.json
        _trainerEmail = _json.get('trainerEmail', None)
        _firstName = _json.get('firstName', None)
        _lastName = _json.get('lastName', None)
        _gender = _json.get('gender', None)
        _state = _json.get('state', None)
        _city = _json.get('city', None)
        _mobileNumber = _json.get('mobileNumber', None)
        _aboutMe = _json.get('aboutMe', None)

        if _firstName.strip() == "":
            return "First name is empty", 400
        
        if _trainerEmail.strip() == "":
            return "Trainer email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('InsertOrUpdateTrainer',(_firstName, _lastName, _gender, _state, _city, _mobileNumber, _trainerEmail, _aboutMe))
        if cur.rowcount > 0:
            return "Trainer updated successfully"
        else:
            return "Failed to update trainer", 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()