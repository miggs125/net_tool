import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "192.168.0.1"

def pscan(port):
    try:
        s.connect((socket.gethostname(), port))
        return True
    except:
        return False

for port in range(1,4000):
    if pscan(port):
        print(f"port {port} is open")