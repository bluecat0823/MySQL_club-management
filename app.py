from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1q2w3e4r",
    "database": "club_management"
}

# 데이터베이스 연결 함수
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return """
    <h1>Welcome to Club Management System</h1>
    <p>Use the following endpoints to manage students:</p>
    <ul>
        <li>POST /students - Add a student</li>
        <li>PUT /students/&lt;id&gt; - Update a student</li>
        <li>DELETE /students/&lt;id&gt; - Delete a student</li>
    </ul>
    """


# 회원 추가 (Create)
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO students (name, birth_date, grade, department, phone_number, is_graduated)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data['name'], data['birth_date'], data['grade'], data['department'], data['phone_number'], data['is_graduated']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201

# 회원 수정 (Update)
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE students
    SET name = %s, birth_date = %s, grade = %s, department = %s, phone_number = %s, is_graduated = %s
    WHERE id = %s
    """
    cursor.execute(query, (data['name'], data['birth_date'], data['grade'], data['department'], data['phone_number'], data['is_graduated'], student_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student updated successfully"}), 200

# 회원 삭제 (Delete)
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
