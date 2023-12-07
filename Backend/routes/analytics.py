from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

app_analytics = Blueprint('app_analytics',__name__)

@app_analytics.route('/top-exercise', methods=['GET'])
def get_client():
    try:
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetTopExercises')
        
        data = cur.fetchall()
        exercises = []
        for exercise in data:
            topExercise = {
                "exercise_name": exercise[0],
                "exercise_count": exercise[1],
            }
            exercises.append(topExercise)
        return jsonify(exercises)
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_analytics.route('/top-body-parts', methods=['GET'])
def get_top_body_parts():
    try:
        connection = get_db()
        cur = connection.cursor()
        cur.callproc('GetTopBodyParts')
        
        data = cur.fetchall()
        bodyParts = []
        for bodyPart in data:
            topBodyPart = {
                "part_name": bodyPart[0],
                "part_count": bodyPart[1],
            }
            bodyParts.append(topBodyPart)
        return jsonify(bodyParts)
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()
