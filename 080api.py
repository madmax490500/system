from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 설정
db_config = {
    'user': 'root',
    'password': 'passwd',
    'host': '192.168.0.0',
    'database': 'test'
}

# MySQL 연결
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    # 입력 데이터 확인
    if 'id' not in data or 'phone' not in data:
        return jsonify({'error': 'ID and phone number are required'}), 400

    user_id = data['id']
    phone = data['phone']

    # 데이터베이스에 삽입
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO users (id, phone) VALUES (%s, %s)"
        cursor.execute(query, (user_id, phone))
        connection.commit()

        return jsonify({'message': 'User added successfully'}), 201

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Database error'}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

##mysql테이블세팅
##CREATE TABLE users (
##    id VARCHAR(50) NOT NULL,
##    phone VARCHAR(20) NOT NULL,
##    PRIMARY KEY (id)
##);

## API테스트
## curl -X POST http://127.0.0.1:5000/add_user \
##     -H "Content-Type: application/json" \
##     -d '{"id": "user123", "phone": "010-1234-5678"}'
## windows
## curl -X POST http://127.0.0.1:5000/add_user -H "Content-Type: application/json" -d "{\"id\": \"user123\", \"phone\": \"01012345678\"}"
