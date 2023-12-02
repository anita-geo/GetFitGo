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