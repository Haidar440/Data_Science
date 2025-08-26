import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)
def get_user():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='8980@Dev@',
        database='mydb'
    )
    cursor = conn.cursor()
    cursor.execute("select * from users")
    rows = cursor.fetchall()
    conn.close()
    return rows
@app.route('/users',methods=['GET'])
def users():
    users = get_user()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)



