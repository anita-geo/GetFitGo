from flask import Blueprint, jsonify, request
from db import get_db

app_exercise = Blueprint('app_exercise',__name__)

@app_exercise.route('/exercise', methods=['POST'])
def get_exercise():
    _json = request.json
    _id = _json.get('id', None)
    _title = _json.get('title', None)
    _description = _json.get('description', None)
    _type = _json.get('type', None)
    _body_part = _json.get('body_part', None)
    _equipment = _json.get('equipment', None)
    _level = _json.get('level', None)

    connection = get_db()
    cur = connection.cursor()
    cur.callproc('FetchExercises',(_id, _title, _description, _type, _body_part, _equipment, _level))

    data = cur.fetchall() 
    exercises = []
    for exercise_data in data:
        exercise = {
            "id": exercise_data[0],
            "name": exercise_data[1],
            "description": exercise_data[2],
            "type": exercise_data[3],
            "body_part": exercise_data[4],
            "equipment": exercise_data[5],
            "level": exercise_data[6]
        }
        exercises.append(exercise)
    cur.close()
    return jsonify(exercises)

@app_exercise.route('/filter-values', methods=['GET'])
def get_filter_values():
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetFilterValue', ())
            
            result_exercise_type = cursor.fetchall()
            
            cursor.nextset()
            result_body_part = cursor.fetchall()
            
            cursor.nextset()
            result_equipment = cursor.fetchall()
            
            cursor.nextset()
            result_level = cursor.fetchall()

            response_json = {
                'exerciseType': result_exercise_type,
                'bodyPart': result_body_part,
                'equipment': result_equipment,
                'level': result_level
            }

            return response_json

    except Exception as e:
        print(e)
        return "Failed to retrieve filter values", 500

    finally:
        connection.close()