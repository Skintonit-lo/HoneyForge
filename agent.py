import time
import json
import requests

LOG_FILE = "honeypot_web.log"  
CENTER_URL = "http://127.0.0.1:5000/api/attacks"  
LAST_POSITION = 0 

def send_to_center(data):
    try:
        response = requests.post(CENTER_URL, json=data, timeout=5)
        if response.status_code == 200:
            print(f"[+] Отправлено: {data.get('username')}")
        else:
            print(f"[-] Ошибка центра: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Центр недоступен: {e}")

def tail_log():
    global LAST_POSITION
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            f.seek(LAST_POSITION)  
            new_lines = f.readlines()  
            LAST_POSITION = f.tell()  
            
            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)  
                    send_to_center(data)
                except json.JSONDecodeError:
                    print(f"[-] Битая строка: {line}")
    except FileNotFoundError:
        print(f"[-] Файл {LOG_FILE} не найден. Жду...")

if __name__ == "__main__":
    print("[*] Агент запущен. Слежу за логом...")
    while True:
        tail_log()
        time.sleep(5)  