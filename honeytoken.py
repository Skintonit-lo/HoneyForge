import os
import time
import datetime
import json
import requests


TOKEN_FILE = r"C:\Users\1122\Desktop\ЛИЗА\admin_credentials.txt"


CENTER_URL = "http://127.0.0.1:1319/api/event"


CHECK_INTERVAL = 3

def create_token_file():
    if not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write("=== СЕКРЕТНЫЕ ДАННЫЕ ===\n")
            f.write("Логин: admin\n")
            f.write("Пароль: SuperSecret123\n")
            f.write("API-ключ: sk-1234567890abcdef\n")
            f.write("=== НЕ ПЕРЕДАВАТЬ ТРЕТЬИМ ЛИЦАМ ===\n")
        print(f"[*] Honeytoken создан: {TOKEN_FILE}")

def get_file_mtime():
    try:
        return os.path.getatime(TOKEN_FILE)
    except FileNotFoundError:
        return None

def send_alert(event_type, details):
    alert = {
        "time": datetime.datetime.now().isoformat(),
        "ip": "local",
        "username": f"HONEYTOKEN_{event_type}",
        "password": details,
        "user_agent": "Honeytoken Monitor"
    }
    try:
        response = requests.post(CENTER_URL, json=alert, timeout=5)
        if response.status_code == 200:
            print(f"[!] АЛЕРТ ОТПРАВЛЕН: {event_type} — {details}")
        else:
            print(f"[-] Ошибка центра: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Центр недоступен: {e}")

def monitor(): 
    print(f"[*] Honeytoken мониторинг запущен: {TOKEN_FILE}")
    last_atime = get_file_mtime()
    
    while True:
        time.sleep(CHECK_INTERVAL)
        current_atime = get_file_mtime()
        
        if current_atime is None:
            print(f"[-] Файл {TOKEN_FILE} исчез!")
            send_alert("DELETED", "Файл-приманка удалён")
            break
        
        if current_atime != last_atime:
            print(f"[!] ФАЙЛ ОТКРЫТ! Время: {datetime.datetime.fromtimestamp(current_atime)}")
            send_alert("ACCESSED", f"Файл открыт в {datetime.datetime.fromtimestamp(current_atime)}")
            last_atime = current_atime

if __name__ == "__main__":
    create_token_file()
    monitor()