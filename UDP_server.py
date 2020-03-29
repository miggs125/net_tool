import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((socket.gethostname(), 1234))
print("UDP server listening")

while True:
    message, addr = s.recvfrom(1024)
    clientMsg = f"Message from Client:{message}"
    clientIP  = f"Client IP Address:{addr}"
    print(clientMsg)
    print(clientIP)

    s.sendto(b"Hello client", addr)