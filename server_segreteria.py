import json  # Importa il modulo JSON per lavorare con i dati JSON
import socket  # Importa il modulo socket per le connessioni di rete
import sys  # Importa il modulo sys per la gestione del sistema
import threading  # Importa il modulo threading per gestire i thread
import tkinter  # Importa il modulo tkinter per creare interfacce grafiche

class SecretaryServer:

    def __init__(self, host="localhost", port=10001, uni_server_host='localhost', uni_server_port=10000):
        # Inizializza il server della segreteria
        self.host = host  # Indirizzo host del server della segreteria
        self.port = port  # Porta del server della segreteria
        self.uni_server_host = uni_server_host  # Indirizzo host del server dell'università
        self.uni_server_port = uni_server_port  # Porta del server dell'università
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
        self.server_socket.bind((self.host, self.port))  # Associa il socket all'indirizzo e alla porta
        self.server_socket.listen(5)  # Mette il server in ascolto di connessioni in entrata(con un massimo di 5)
        print(f"Server in ascolto su {self.host}:{self.port}")

    def handle_student_connection(self, client_socket):
        # Gestisce la connessione con uno studente
        try:
            while True:
                request = client_socket.recv(4096).decode('utf-8')  # Riceve i dati dal client
                if not request:
                    break  # Esce dal ciclo se non ci sono più dati
                request_data = json.loads(request)  # Decodifica i dati ricevuti in formato JSON
                
                # Inoltra i dati al server dell'università se necessario
                #se la richiesta dello studente è quella di visualizzare gli esami allora viene gestita direttamente da questo server
                if request_data["type"] == "viewExams":
                    print("Me ne occupo io")
                    seg_management = self.get_exams_data()  # Ottiene i dati degli esami
                    seg_reponse = json.dumps(seg_management)  # Codifica i dati degli esami in JSON
                    client_socket.sendall(seg_reponse.encode('utf-8'))  # Invia i dati al client
                else:
                    uni_response = self.forward_request_to_university_server(request_data)  # Inoltra la richiesta al server dell'università
                    rispostaUni = json.dumps(uni_response)  # Codifica la risposta del server dell'università in JSON
                    print(rispostaUni)
                    client_socket.sendall(rispostaUni.encode('utf-8'))  # Invia la risposta al client
        finally:
            client_socket.close()  # Chiude la connessione con il client
    
    def get_exams_data(self):
        # Ottiene i dati degli esami
        try:
            with open("esami.json", "r") as f:
                data = json.load(f)  # Carica i dati dal file JSON
                if data is not None:
                    # Se i dati sono validi, li stampa e li restituisce
                    for exam in data:
                        print(f"Esame: {exam['nome']}, Data: {exam['data']}")
                    return data
                else:
                    print("Dati non disponibili o vuoti")
        except FileNotFoundError:
            print("File non trovato")
        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare JSON: {e}")

    def forward_request_to_university_server(self, request_data):
        # Inoltra la richiesta al server dell'università e ottiene la risposta
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as uni_socket:
            uni_socket.connect((self.uni_server_host, self.uni_server_port))  # Connette al server dell'università
            uni_socket.sendall(json.dumps(request_data).encode('utf-8'))  # Invia i dati al server dell'università
            response = uni_socket.recv(4096).decode('utf-8')  # Riceve la risposta dal server dell'università
            return json.loads(response)  # Decodifica la risposta in formato JSON

    def start(self):
        # Avvia il server e accetta le connessioni dei client
        while True:
            client_sock, client_address = self.server_socket.accept()  # Accetta una nuova connessione
            print(f"Connessione Accettata da Client {client_address}")
            # Crea un nuovo thread per gestire la connessione in modo che il server possa servire più studenti contemporaneamente
            client_handler = threading.Thread(target=self.handle_student_connection, args=(client_sock,))
            client_handler.start()  # Avvia il thread

if __name__ == "__main__":
    # Crea e avvia il server della segreteria
    secretary_server = SecretaryServer()
    secretary_server.start()
