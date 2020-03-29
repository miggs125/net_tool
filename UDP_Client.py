import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(b"hello server", (socket.gethostname(), 1234))
data, addr = s.recvfrom(1024)
print(data)