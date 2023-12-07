from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

app_client = Blueprint('app_client',__name__)

@app_client.route('/view-client', methods=['GET'])
def get_client():
    try:
        _clientEmail = request.args.get('clientEmail', None)

        if _clientEmail.strip() == "":
            return "Client email is empty", 400

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetClientInfo',(_clientEmail, None))
        
        data = cur.fetchall()
        data = data[0]
        
        cur.callproc('GetClientDetailsByEmail', (_clientEmail,))

        result_body_parts = cur.fetchall()
        
        cur.nextset()

        result_equipments = cur.fetchall()

        cur.nextset()

        result_routines = cur.fetchall()

        cur.nextset()

        result_diet_type = cur.fetchall()

        client = {
            "clientEmail": data[0],
            "firstName": data[1],
            "lastName": data[2],
            "gender": data[3],
            "height": data[4],
            "weight": data[5],
            "targetWeight": data[6],
            "bodyType": data[7],
            "aboutMe": data[8],
            "level": data[9],
            "trainerEmail": data[10],
            'bodyParts': [row[0] for row in result_body_parts],
            'equipments': [row[0] for row in result_equipments],
            'dietType': [row[1] for row in result_diet_type],
            'routines': [row[1] for row in result_routines],
        }
        return jsonify(client)
        
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/update-client', methods=['POST'])
def update_client():
    try:
        _json = request.json
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

        if _email.strip() == "":
            return "Email is empty", 400
        
        if _firstName.strip() == "":
            return "First name is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('InsertOrUpdateClient',(_email, _firstName, _lastName, _gender,_streetNo,_streetName,_city,  _state, _mobileNumber, _height, _weight,_bodyType, _bmi,_targetWeight, _level, _aboutMe))
        if cur.rowcount > 0:
            return "Client updated successfully"
        else:
            return "Failed to update client", 500
        
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/view-workouts', methods=['POST'])
def get_workouts():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _logDate = _json.get('logDate', None)

        if _clientEmail.strip() == "":
            return "Client email is empty", 400

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetClientLogsDetailed', (_clientEmail, _logDate))
            
        result = cur.fetchall()

        workouts = []
        for row in result:
            log_entry = {
                'id': row[0],
                'exercise_id': row[1],
                'email': row[2],
                'reps': row[3],
                'date': str(row[4]),
                'title': row[5],
                'description': row[6],
                'type': row[7],
                'body_part': row[8],
                'equipment': row[9],
                'level': row[10]
            }
            workouts.append(log_entry)

        return jsonify(workouts)
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/log-workout', methods=['POST'])
def log_workout():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _exerciseId = _json['exerciseId']
        _reps = _json['reps']

        if _clientEmail.strip() == "":
            return "client email is empty", 400

        if _exerciseId == 0:
            return "Exercise id should be greater than 0", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('InsertClientLogsExercise',( _exerciseId, _clientEmail, _reps,))
      
        if cur.rowcount > 0:
            return "Logged workout successfully"
        else:
            return "Failed to log workout", 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/delete-workout', methods=['DELETE'])
def delete_workout():
    try:
        _id = request.args.get('id', None)
        _clientEmail = request.args.get('clientEmail', None)

        if _clientEmail.strip() == "":
            return "Client email is empty", 400

        if _id == 0:
            return "Id is required", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('DeleteClientWorkout',(_clientEmail, _id,))
        
        if cur.rowcount > 0:
            return "Delete workout log"
        else:
            return "Failed to delete workout log", 500
    except pymysql.MySQLError as e:
        return e.args[1], 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/view-assigned-routine', methods=['GET'])
def get_assigned_routine():
    try:
        _clientEmail = request.args.get('clientEmail', None)

        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('ViewClientRoutine',(_clientEmail,))
        
        data = cur.fetchall() 
        grouped_results = {}

        for row in data:
            # Extract routine-related information
            routine_id = row[0]
            routine_name = row[1]
            routine_description = row[2]

            # Extract exercise-related information
            exercise_id = row[3]
            exercise_title = row[4]
            exercise_description = row[5]
            reps = row[6]

            # Create an exercise dictionary
            if exercise_id != None:
                exercise = {
                    "exercise_id": exercise_id,
                    "exercise_title": exercise_title,
                    "exercise_description": exercise_description,
                    "reps": reps
                }
            else:
                exercise = None

            if routine_id in grouped_results:
                grouped_results[routine_id]['exercises'].append(exercise)
            else:
                if exercise is not None:
                    grouped_results[routine_id] = {
                        "routine_id": routine_id,
                        "routine_name": routine_name,
                        "routine_description": routine_description,
                        "exercises": [exercise]
                    }
                else:
                    grouped_results[routine_id] = {
                        "routine_id": routine_id,
                        "routine_name": routine_name,
                        "routine_description": routine_description,
                        "exercises": []
                    }

        result_list = list(grouped_results.values())
        return jsonify(result_list)
    except Exception as e:
        connection.rollback()
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/view-assigned-diet', methods=['GET'])
def get_assigned_diet():
    try:
        _clientEmail = request.args.get('clientEmail', None)
    
        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('ViewClientDiets',(_clientEmail,))
        
        data = cur.fetchall() 
        diets = []
        for diet_data in data:
            diet = {
                "dietId": diet_data[0],
                "dietName": diet_data[1],
                "breakfast": diet_data[2],
                "lunch": diet_data[3],
                "dinner": diet_data[4],
                "instruction": diet_data[5]
            }
            diets.append(diet)

        return jsonify(diets)
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/add-client-equipment', methods=['POST'])
def add_client_equipment():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _equipment_names = _json.get('equipmentNames', [])

        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        if not _equipment_names:
            return "Equipment names list is empty", 400
        
        json_data = jsonify(_equipment_names).get_data(as_text=True)

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('InsertClientEquipment',(_clientEmail, json_data))
        
        return "Inserted client equipment"

    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/delete-client-equipment', methods=['DELETE'])
def delete_client_equipment():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _equipment = _json['equipment']
    
        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        if _equipment.strip() == "":
            return "Equipment is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('DeleteClientEquipment',(_clientEmail, _equipment,))
        
        if cur.rowcount > 0:
            return "Deleted client equipment"
        else:
            return "Failed to delete client equipment", 500

    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/add-client-body-part', methods=['POST'])
def add_client_body_part():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _bodyParts = _json.get('bodyParts', [])

        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        if not _bodyParts:
            return "Body part names list is empty", 400
        
        json_data = jsonify(_bodyParts).get_data(as_text=True)
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('InsertClientTrainingForBodyPart',(_clientEmail, json_data))
        
        return "Inserted client training for body part"

    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_client.route('/delete-client-body-part', methods=['DELETE'])
def delete_client_body_part():
    try:
        _json = request.json
        _clientEmail = _json['clientEmail']
        _bodyPart = _json['bodyPart']
    
        if _clientEmail.strip() == "":
            return "Client email is empty", 400
        
        if _bodyPart.strip() == "":
            return "Body part is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('DeleteClientBodyPart',(_clientEmail, _bodyPart,))
        
        if cur.rowcount > 0:
            return "Deleted client training body part"
        else:
            return "Failed to delete client training body part", 500

    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()