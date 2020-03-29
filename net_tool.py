#!/usr/bin/env python 

'''
This program can be used to start a server or a client using sockets.
'''

import sys
import os
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print("*"*100)
    print("*"*44," NET TOOL ","*"*44)
    print("*"*100, "\n")
    print("Usage ./net_tool -t <target host> -p <target port>\n")
    print("-l --listen\t- listen on [host]:[port] for incoming connections\n".
          expandtabs(40))
    print(
        "-e --execute-file=<path_to_file>\t- execute a given file upon receiving a connection\n"
    )
    print("-c --command\t- initialize a command shell\n".expandtabs(40))
    print(
        "-u --upload=<destination>\t- upon receiving connection, upload a file and write\n\t  to <destination>"
        .expandtabs(40))
    
    print ("\n\n")
    print("Examples:")
    print("./net_tool.py -t 127.0.0.1 -p 8080 -l -c")
    print("./net_tool.py -t 127.0.0.1 -p 8080 -l -c -u=path/to/file")
    print("./net_tool.py -t 127.0.0.1 -p 8080 -l -c -e=\"cat /some/file\"")
    print("echo 'hello' | ./net_tool.py -t 192.168.10.15 -p 80 ")
    sys.exit(0)


def main():
    global listen
    global port
    global upload
    global command
    global target
    global upload_destination
    global execute

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", 
            ["help", "listen", "execute=", "target=", "port=", "command-shell", "upload="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    # handle options    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in  ("-c", "--command-shell"):
            command = True
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-u", "-upload"):
            upload_destination = a
        else:
            assert False, "Unhandled option"

    # send data to target
    if not listen and len(target) and port > 0:  
        client_sender("")
    
    if listen:
        start_server()
        
def client_sender(buffer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((target, port))       

        while True:
            response = ""
            msg_length = 1
            while msg_length:
                msg = s.recv(4096).decode("utf-8")
                print(msg)
                msg_length = len(msg)
                if msg_length < 4096:
                    break
                else:
                    response += msg
            
            print(response.rstrip(), end="")
            
            # wait for more input
            buffer = input("")
            buffer += "\n"
            
            s.send(buffer.encode())
    except Exception as e:
        print(e)
        s.close()
    
    
def start_server():
    global target
    
    if not len(target):
        target = "0.0.0.0"
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((target, port))
    s.listen(5)
    print(f"Listening on port {port}")
    
    while True:
        client_socket, address = s.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()
        print(f"connection from {address} has been established")

def run_command(command):
    command = command.rstrip() # remove new-line

    cmd = subprocess.check_output(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = cmd.stdout.read() + cmd.stderr.read()
    output_str = str(output, "utf_8")
    
    return output_str

def client_handler(client_socket):
    if len(upload_destination):
        file_buffer = ""
        
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break;
            
            file_buffer += data
            
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            client_socket.send("Successfully saved file".encode())
        except:
            client_socket.send("Failed to save file".encode())
    
    if len(execute):
        output = run_command(execute).decode("utf-8")
        
        client_socket.send(output.encode("utf-8"))
    
    if command:
        
        while True:
            cmd = input()
            if cmd == "quit":
                client_socket.close()
                
            
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                response = str(run_command(data), "utf-8")
          
            client_socket.send(response.encode())
        # while True:
        #     client_socket.send(("terminal $ ").encode())
        #     cmd_buffer = ""
        #     while "\n" not in cmd_buffer:
        #         cmd_buffer = client_socket.recv(1024).decode("utf-8")
        #         print("BUFFER: ", cmd_buffer)                
        #         response = str(run_command(cmd_buffer), "utf-8")

                    
main()