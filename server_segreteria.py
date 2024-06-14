import json
import socket
import sys
import threading
import tkinter

class SecretaryServer:

    def __init__(self, host="localhost", port = 10001, uni_server_host = 'localhost', uni_server_port = 10000):
        self.host = host
        self.port = port
        self.uni_server_host = uni_server_host
        self.uni_server_port = uni_server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen(5)
        print(f"Server in ascolto su {self.host}:{self.port}")

    def handle_student_connection(self,client_socket):
        try:
            while True:
                request = client_socket.recv(4096).decode('utf-8')
                if not request:
                    break
                request_data = json.loads(request)
                #inoltra i dati al server dell'università
                uni_response = self.forward_request_to_university_server(request_data)
                #inoltriamo la response dell'uni al client studente
                rispostaUni = json.dumps(uni_response)
                print(rispostaUni)
                client_socket.sendall(rispostaUni.encode('utf-8'))
        finally:
            client_socket.close()

    def forward_request_to_university_server(self,request_data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as uni_socket:
            uni_socket.connect((self.uni_server_host, self.uni_server_port))
            uni_socket.sendall(json.dumps(request_data).encode('utf-8'))
            response = uni_socket.recv(4096).decode('utf-8')
            return json.loads(response)


    def start(self):
        while True:
            client_sock, client_address = self.server_socket.accept()
            print(f"Connessione Accettata da Client {client_address}")
             # Crea un nuovo thread per gestire la connessione in modo che il server possa servire più studenti contemporaneamente
            client_handler = threading. Thread(target = self.handle_student_connection, args = (client_sock,))
            client_handler.start() #Avvia Thread

if __name__ == "__main__":
    secretary_server = SecretaryServer()
    secretary_server.start()























