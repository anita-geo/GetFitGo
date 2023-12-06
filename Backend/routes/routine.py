from flask import Blueprint, jsonify, g, request
from db import get_db
import pymysql

app_routine = Blueprint('app_routine',__name__)

@app_routine.route('/routine', methods=['GET'])
def get_routine():
    _trainerEmail = request.args.get('trainerEmail', None)

    if _trainerEmail.strip() == "":
        return "Trainer email is empty", 400
    
    connection = get_db()
    cur = connection.cursor()
    cur.callproc('ViewTrainerRoutine',(_trainerEmail,))

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

        # Check if routine_id is already a key in the grouped_results dictionary
        if routine_id in grouped_results:
            # If yes, append the exercise to the existing list
            grouped_results[routine_id]['exercises'].append(exercise)
        else:
            # If no, create a new entry for the routine with the exercise list
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

    # Convert the values of the dictionary to a list
    result_list = list(grouped_results.values())
    cur.close()
    connection.close()
    return jsonify(result_list)

@app_routine.route('/routine', methods=['POST'])
def create_routine():
    try:
        _json = request.json
        _name = _json['routineName']
        _description = _json['routineDescription']
        _trainerEmail = _json['trainerEmail']

        connection = get_db()
        cur = connection.cursor()

        sql = 'INSERT INTO routine (name, description, trainer_email) VALUES (%s, %s, %s)'
        cur.execute(sql, (_name, _description, _trainerEmail))
        if cur.rowcount > 0:
            return jsonify({"success": "Routine inserted successfully"})
        else:
            connection.rollback()
            return jsonify({"error": "Failed to insert routine"}), 500
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_routine.route('/routine', methods=['DELETE'])
def delete_routine():
    try:
        _routineId = request.args.get('routineId', None)
    
        connection = get_db()
        cur = connection.cursor()

        sql = 'DELETE FROM routine where routine_id = %s'
        cur.execute(sql, (_routineId))

        if cur.rowcount > 0:
            return jsonify({"success": "Routine deleted successfully"})
        else:
            connection.rollback()
            return jsonify({"error": "Failed to delete routine"}), 500
        
    except pymysql.MySQLError as e:
        return e.args[1], 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

# --------- Routine Exercise ------------------

@app_routine.route('/routine-exercise', methods=['POST'])
def add_routine_exercise():
    try:
        _json = request.json
        _exercises = _json['exercises']
        _routineId = _json['routineId']

        if _routineId == 0 or _routineId is None:
            return "Trainer email is empty", 400
        
        connection = get_db()
        cur = connection.cursor()
        json_data = jsonify(_exercises).get_data(as_text=True)
        cur.callproc('AddExerciseToRoutine', (json_data, _routineId))

        if cur.rowcount > 0:
            return jsonify({"success": "Exercise added to routine successfully"})
        else:
            connection.rollback()
            return jsonify({"error": "Failed to insert routine"}), 500
    
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_routine.route('/routine-exercise', methods=['DELETE'])
def delete_routine_exercise():
    try:
        _json = request.json
        _routineId = _json['routineId']
        _exerciseId = _json['exerciseId']

        if _routineId == 0 or _routineId is None:
            return "Routine id should be greater than 0", 400
        
        if _exerciseId == 0 or _exerciseId is None:
            return "Exercise id should be greater than 0", 400
        
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('RemoveExerciseFromRoutine', (_routineId, _exerciseId))
        
        return 'Successfully removed exercise from routine'
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_routine.route('/routine-rep', methods=['POST'])
def update_routine_rep():
    try:
        _json = request.json
        _routineId = _json['routineId']
        _exerciseId = _json['exerciseId']
        _reps = _json['reps']

        connection = get_db()
        cur = connection.cursor()

        cur.callproc('UpdateRoutineRep',(_routineId, _exerciseId, _reps))
        
        return 'Successfully updated exercise reps'
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()


# --------- Assign Routine --------

@app_routine.route('/routine-assign', methods=['POST'])
def assign_routine():
    try:
        _json = request.json
        _trainerEmail = _json['trainerEmail']
        _clientEmail = _json['clientEmail']
        _routines = _json['routines']

        connection = get_db()
        cur = connection.cursor()

        json_data = jsonify(_routines).get_data(as_text=True)

        cur.callproc('AssignRoutineToClient',(_trainerEmail, _clientEmail, json_data))
        
        return 'Successfully assigned routine to user'
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_routine.route('/routine-unassign', methods=['DELETE'])
def unassign_routine():
    try:
        _id = request.args.get('id', None)

        connection = get_db()
        cur = connection.cursor()

        sql = 'UPDATE trainer_allocates_routine SET end_date = current_date() where id = %s'
        cur.execute(sql, (_id))
        
        return 'Successfully unassigned routine'
    except pymysql.MySQLError as e:
        if e.args[0] == 45000:
            print("Caught SQLSTATE 45000 error: ", e)
        return 'Something went wrong', 500
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()