from flask import Blueprint, request, jsonify
from my_database_lib import db, SECRET_KEY
import jwt
from my_database_lib.models import User,Todo

SECRET_KEY = 'secretkey'

todo_blueprint = Blueprint('todo', __name__)

def decode_token():
    token = request.headers.get('Authorization')
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decode_data
    except jwt.ExpiredSignatureError:
        return {'error':'Token has expired'}
    except jwt.InvalidTokenError:
        return {"error":"Invalid token"}


@todo_blueprint.route('/todos', methods=['POST'])
def create_todo():
    title = request.json.get("title")
    description = request.json.get("description")
    decode_data=decode_token()
    if 'error' in decode_data:
        return jsonify({"messgae":decode_data['error']})
    
    current_user = decode_data.get("username")

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    new_todo = Todo(title=title, description=description, user_id=user.id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201

@todo_blueprint.route('/gettodo',methods=['GET'])
def gettodo():
    decode_data=decode_token()
    if 'error' in decode_data:
        return jsonify({"messgae":decode_data['error']})
    current_user=decode_data.get('username')
    user=User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message':'user not registerd'})
    user_id=user.id
    todo_list=Todo.query.filter_by(user_id=user_id).all()
    todo_list_dicts = [todo.to_dict() for todo in todo_list] 
    return jsonify({'data': todo_list_dicts}), 200

@todo_blueprint.route('update_todo/<int:id>',methods=['PUT'])
def update_todo(id):
    description=request.json.get('description')
    decode_data=decode_token()
    if 'error' in decode_data:
        return jsonify({"messgae":decode_data['error']})
    current_user=decode_data.get('username')

    user=User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message':"user not authorized"}),400
    
    todo_query=Todo.query.filter_by(id=id,user_id=user.id).first()
    if not todo_query:
        return jsonify({"message":"no notes found "}),404

    todo_query.description=description
    db.session.commit()

    return jsonify({'message':'todo_updated'}),200


@todo_blueprint.route('delete_todo/<int:id>',methods=['DELETE'])
def delete_todo(id):
    decode_data=decode_token()
    if 'error' in decode_data:
        return jsonify({"messgae":decode_data['error']})
    current_user=decode_data.get("username")

    user=User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'message':'user not found'}),404

    todo_query=Todo.query.filter_by(id=id,user_id=user.id).first()

    if not todo_query:
        return jsonify({'message':'no notes to delete'}),400
    
    db.session.delete(todo_query)
    db.session.commit()

    return jsonify({"message":"notes delete"}),201