from flask import Flask, request, jsonify
from flask_cors import CORS  
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = "attacks.db" 

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            ip TEXT,
            username TEXT,
            password TEXT,
            user_agent TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/api/attacks', methods=['POST'])
def receive_attack():
    data = request.get_json() 
    
    if not data:
        return jsonify({"error": "Нет данных"}), 400
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attacks (time, ip, username, password, user_agent)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get('time'),
        data.get('ip'),
        data.get('username'),
        data.get('password'),
        data.get('user_agent')
    ))
    conn.commit()
    conn.close()
    
    print(f"[+] Получена атака: {data.get('username')} / {data.get('password')}")
    return jsonify({"status": "ok"}), 200

@app.route('/api/attacks', methods=['GET'])
def get_attacks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attacks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    attacks = []
    for row in rows:
        attacks.append({
            "id": row[0],
            "time": row[1],
            "ip": row[2],
            "username": row[3],
            "password": row[4],
            "user_agent": row[5]
        })
    
    return jsonify(attacks)

if __name__ == '__main__':
    init_db()  
    print("[*] Центр запущен на порту 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)