from flask import Blueprint, jsonify, request
from db import get_db
import pymysql

app_diet = Blueprint('app_diet',__name__)

@app_diet.route('/diet', methods=['GET'])
def get_diet():
    try:
        _dietType = request.args.get('dietType', None)

        connection = get_db()
        cur = connection.cursor()
        cur.callproc('ViewDiets',(_dietType,))
        
        data = cur.fetchall() 
        diets = []
        for diet_data in data:
            diet = {
                "dietId": diet_data[0],
                "dietName": diet_data[1],
                "breakfast": diet_data[2],
                "lunch": diet_data[3],
                "dinner": diet_data[4],
                "instruction": diet_data[5],
                "trainerEmail": diet_data[6]
            }
            diets.append(diet)

        return jsonify(diets)
    except pymysql.MySQLError as e:
        print(e)
    except Exception as e:
        connection.rollback()
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_diet.route('/diet', methods=['POST'])
def create_diet():
    try:
        _json = request.json
        _dietId = _json.get('dietId', None)
        _trainerEmail = _json['trainerEmail']
        _dietType = _json['dietType']
        _breakfast = _json['breakfast']
        _lunch = _json['lunch']
        _dinner = _json['dinner']
        _instruction = _json['instruction']
        
        connection = get_db()
        cur = connection.cursor()

        if _dietId is None:
            cur.callproc('CreateDiet',(_trainerEmail, _dietType, _breakfast, _lunch, _dinner, _instruction))
        else:
            cur.callproc('EditDiet',(_trainerEmail, _dietId, _breakfast, _lunch, _dinner, _instruction))
        
        if cur.rowcount > 0:
           return "Diet created/updated successfully"
        else:
            return "Failed to create diet", 500
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

@app_diet.route('/diet', methods=['DELETE'])
def delete_diet():
    try:
        _json = request.json
        _dietId = _json['dietId']
        _trainerEmail = _json['trainerEmail']
        
        connection = get_db()
        cur = connection.cursor()

        cur.callproc('DeleteDiet',(_trainerEmail, _dietId))
        
        if cur.rowcount > 0:
           return "Diet deleted successfully"
        else:
            return "Failed to delete diet", 500
    except pymysql.MySQLError as e:
        if len(e.args) > 1:
            return e.args[1], 500
        return 'Something went wrong', 500
    except Exception as e:
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()

@app_diet.route('/assign-diet', methods=['POST'])
def assign_diet():
    try:
        _json = request.json
        _dietName = _json['dietName']
        _trainerEmail = _json['trainerEmail']
        _clientEmail = _json['clientEmail']
        
        connection = get_db()
        cur = connection.cursor()

        cur.callproc('AssignDietTypeToUser',(_dietName, _trainerEmail, _clientEmail))
        
        if cur.rowcount > 0:
           return "Diet assigned to user successfully"
        else:
            return "Failed to assign diet to user", 500
    except pymysql.MySQLError as e:
        if len(e.args) > 1:
            return e.args[1], 500
        return 'Something went wrong', 500
    except Exception as e:
        return "Something went wrong", 500
    finally:
        cur.close()
        connection.close()