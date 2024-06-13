import json
import socket
import sys
import threading
import tkinter

class UniversityServer:

    def __init__(self,host='localhost',port=10000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client_connection(self, client_socket):
        while True:
            try:
                request = client_socket.recv(4096).decode('utf-8')
                if not request:
                    break
                request_data = json.loads(request)
                response_data = self.process_request(request_data)
                client_socket.sendall(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(f"Errore {e}")
                break
        client_socket.close()
    
    def process_request(self,request):
        try:
            if 'type' not in request:
                return {'error':"Reuqest type is missing"}
            
            if request['type'] == 'login':
                with open("studenti.json",'r')as f:
                    users = json.load(f)
                    response = {"status": "fail"}
                    for user in users:
                        if user["username"] == request["username"] and user["psw"] == request["password"]:
                            response["status"] = "success"
                            break 
                    return response
        except Exception as e:
            print(f"Errore {e}")        

    def start(self):
        print("Starting Server...")
        while True:
            client_sock, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")  # Stampa l'indirizzo del client connesso.
            client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock,))
            client_handler.start()
    



if __name__ == '__main__':
    server = UniversityServer()
    server.start()












