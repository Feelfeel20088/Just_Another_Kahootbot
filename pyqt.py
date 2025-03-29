import sys
import requests
import subprocess
import psutil
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox
from PyQt6.QtCore import QThread, pyqtSignal

def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill the process running on the given port if possible."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    proc.terminate()
                    proc.wait()
                    return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

class APIThread(QThread):
    log_signal = pyqtSignal(str)

    def run(self):
        if is_port_in_use(8000):
            self.log_signal.emit("Port 8000 is in use, terminating conflicting process...")
            kill_process_on_port(8000)  # Ensure port is free before starting API
            self.log_signal.emit("Port 8000 freed and API starting...")
        
        process = subprocess.Popen(
            ["python3", "-u", "__main__.py"],  # -u makes output unbuffered
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        first_websocket_url_logged = False
        first_403_logged = False
        last_challenge_output = None

        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            
            if "Running on" in line:
                self.log_signal.emit("API server started on port 8000.")
            elif "Bot" in line and "connected" in line:
                bot_number = line.split("Bot")[-1].strip()
                self.log_signal.emit(f"Bot {bot_number} successfully connected.")
            elif "Challenge output:" in line:
                if "WebSocket URL:" in line:
                    if not first_websocket_url_logged:
                        self.log_signal.emit(f"WebSocket URL: {line.split('WebSocket URL:')[-1].strip()}")
                        first_websocket_url_logged = True
                elif line != last_challenge_output:  # Log only if the challenge output changes
                    last_challenge_output = line
                    self.log_signal.emit(f"Challenge output: {line}")
            elif "server rejected WebSocket connection: HTTP 403" in line:
                if not first_403_logged:
                    self.log_signal.emit("Error: WebSocket connection rejected (HTTP 403).")
                    first_403_logged = True
            else:
                # Ignore unnecessary lines
                pass
        
        process.stdout.close()
        process.wait()

class KahootBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.api_thread = None
        self.init_ui()
        self.start_api()
    
    def init_ui(self):
        self.setWindowTitle("Kahoot Bot Controller")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()
        
        self.label_gamepin = QLabel("Game PIN:")
        self.input_gamepin = QLineEdit()
        layout.addWidget(self.label_gamepin)
        layout.addWidget(self.input_gamepin)

        self.label_amount = QLabel("Number of Bots:")
        self.input_amount = QLineEdit()
        layout.addWidget(self.label_amount)
        layout.addWidget(self.input_amount)
        
        self.label_nickname = QLabel("Bot Nickname:")
        self.input_nickname = QLineEdit()
        layout.addWidget(self.label_nickname)
        layout.addWidget(self.input_nickname)

        self.label_ttl = QLabel("Bot TTL (seconds):")
        self.input_ttl = QLineEdit()
        layout.addWidget(self.label_ttl)
        layout.addWidget(self.input_ttl)
        
        self.checkbox_crash = QCheckBox("Crash Mode")
        layout.addWidget(self.checkbox_crash)
        
        self.start_button = QPushButton("Start Swarm")
        self.start_button.clicked.connect(self.send_request)
        layout.addWidget(self.start_button)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        self.setLayout(layout)
    
    def start_api(self):
        self.log_output.append("Starting API server...")
        self.api_thread = APIThread()
        self.api_thread.log_signal.connect(self.log_output.append)
        self.api_thread.start()
    
    def closeEvent(self, event):
        if self.api_thread:
            self.log_output.append("Stopping API server...")
            self.api_thread.terminate()
        event.accept()

    def send_request(self):
        url = "http://localhost:8000/swarm"
        
        try:
            data = {
                "amount": int(self.input_amount.text()),
                "gamepin": int(self.input_gamepin.text()),
                "nickname": self.input_nickname.text(),
                "crash": self.checkbox_crash.isChecked(),
                "ttl": int(self.input_ttl.text())
            }
            
            response = requests.post(url, json=data)
            self.log_output.append(f"Response: {response.text}")
        except Exception as e:
            self.log_output.append(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KahootBotGUI()
    window.show()
    sys.exit(app.exec())
