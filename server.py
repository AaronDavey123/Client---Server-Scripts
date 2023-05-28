import socket
import threading  # allows you to run mutiplue thread in python

#every data send will be fitted to a length of 64
HEADER = 64
# find a port that isn't being used
PORT = 5050
# gets ip address automatically
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# UCS Transofrmation Format 8
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# we create a IPv4 socket 'AF_INET' and stream data
# through the socket 'SOCK_STREAM'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Binded address to the socket so anything data that hits the address hits the socket
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        #capture data and decode 
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)                          
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")                                   # 'conn' creates a socket object and allows use to 
            conn.send("Message received From [Server]".encode(FORMAT))                   # communincate back to the object that has connected 

    conn.close()                                                      
                                                                                      
                                               
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
