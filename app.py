from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import datetime

app = Flask(__name__)

mock_users_db = []
next_user_id = 1


def save_user_to_db(user_data):
    global next_user_id
    user_data['user_id'] = next_user_id
    user_data['created_at'] = datetime.datetime.now()
    user_data['updated_at'] = datetime.datetime.now()
    user_data['is_approved'] = False if user_data['user_type'] in ['resident', 'instructor'] else True
    mock_users_db.append(user_data)
    next_user_id += 1
    print(f"DEBUG: User saved: {user_data}")
    return user_data


def get_user_by_email(email):
    for user in mock_users_db:
        if user['email'] == email:
            return user
    return None


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['email', 'password', 'first_name', 'last_name', 'user_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    user_type = data['user_type']

    valid_user_types = ['resident', 'manager', 'instructor', 'admin']
    if user_type not in valid_user_types:
        return jsonify({"message": "Invalid user type provided."}), 400

    if get_user_by_email(email):
        return jsonify({"message": "User with this email already exists."}), 409

    hashed_password = generate_password_hash(password)

    new_user_data = {
        'email': email,
        'password_hash': hashed_password,
        'first_name': first_name,
        'last_name': last_name,
        'user_type': user_type,
        'phone_number': data.get('phone_number'),
        'date_of_birth': data.get('date_of_birth'),
        'address': data.get('address')
    }

    saved_user = save_user_to_db(new_user_data)

    response_user_data = {
        "user_id": saved_user['user_id'],
        "email": saved_user['email'],
        "first_name": saved_user['first_name'],
        "last_name": saved_user['last_name'],
        "user_type": saved_user['user_type'],
        "is_approved": saved_user['is_approved'],
        "message": "User registered successfully." + (" Awaiting approval." if not saved_user['is_approved'] else "")
    }
    return jsonify(response_user_data), 201


if __name__ == '__main__':
    print("OpenNet Backend starting...")
    print("Access the API at http://127.0.0.1:5000/api/register (POST requests)")
    app.run(debug=True)
