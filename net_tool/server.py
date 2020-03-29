# def start_server():
#     global target
    
#     if not len(target):
#         target = "0.0.0.0"
    
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     s.bind((target, port))
#     s.listen(5)
#     print(f"Listening on port {port}")
    
#     while True:
#         client_socket, address = s.accept()
#         client_thread = threading.Thread(target=client_handler, args=(client_socket,))
#         client_thread.start()
#         print(f"connection from {address} has been established")
import socket
import sys
  
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        s = socket.socket()
    except socket.error as msg:
        print("Socket conenction error: " + str(msg))
        
def bind_socket(host, port):
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host,port))
        s.listen(5)

    
        
        