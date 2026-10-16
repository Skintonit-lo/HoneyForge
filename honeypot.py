from flask import Flask, request, render_template
import datetime
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        log_entry = {
            "time": datetime.datetime.now().isoformat(),
            "ip": request.remote_addr, 
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "user_agent": request.headers.get('User-Agent')
        }
        with open("honeypot_web.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            f.flush()
        

        return "Неверный логин или пароль. Попробуйте снова."
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)