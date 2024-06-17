import json
import socket
import threading
from datetime import datetime

class UniversityServer:

    def __init__(self, host='localhost', port=10000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea il socket del server
        self.server_socket.bind((self.host, self.port))  # Assegna l'indirizzo e la porta al socket
        self.server_socket.listen(5)  # Il server ascolta fino a 5 connessioni in attesa
        print(f"Server listening on {self.host}:{self.port}")

    #gestisce la connessione proveniente dal client
    def handle_client_connection(self, client_socket):
        while True:
            try:
                request = client_socket.recv(4096).decode('utf-8')  # Riceve i dati dal client
                if not request:
                    break
                request_data = json.loads(request)  # Decodifica i dati JSON
                response_data = self.process_request(request_data)  # Processa la richiesta
                client_socket.sendall(json.dumps(response_data).encode('utf-8'))  # Invia la risposta al client
            except Exception as e:
                print(f"Errore {e}")
                break
        client_socket.close()  # Chiude la connessione del client

    
    #metodo per gestire prenotazione dell'esame
    def book_Exam(self, request):
        response = {"status": "fail", "booking_number": 0}
        try:
            info = request  # `request` è già un dizionario

            prenotazione = {
                "matricola": info["matricola"],
                "esame": info["esame"],
                "data": info["data"]
            }

            try:
                with open("prenotazioni.json", 'r') as f:
                    prenotazioni = json.load(f)  # Carica le prenotazioni esistenti dal file JSON
            except (FileNotFoundError, json.JSONDecodeError):
                prenotazioni = []

            prenotazione_trovata = False

            #controllo per verificare se la prenotazione associata a quello studente esiste già (intesa con la stessa data)
            for p in prenotazioni:
                if (p["matricola"] == prenotazione["matricola"] and 
                    p["esame"] == prenotazione["esame"] and 
                    p["data"] == prenotazione["data"]):
                    prenotazione_trovata = True
                    break  # Esce dal ciclo una volta trovata la prenotazione

            #counter per gestire numero progressivo delle prenotazioni            
            count_prenotazioni = sum(1 for p in prenotazioni if p["esame"] == prenotazione["esame"] and p["data"] == prenotazione["data"])
            response["booking_number"] = count_prenotazioni + 1  # Genera il numero di prenotazione

            if not prenotazione_trovata: 
                prenotazioni.append(prenotazione)  # Aggiunge la nuova prenotazione
                with open("prenotazioni.json", 'w') as f:
                    json.dump(prenotazioni, f, indent=2)  # Salva le prenotazioni aggiornate nel file JSON
                response["status"] = "success"
        except Exception as e:
            print(f"Errore nella prenotazione dell'esame: {e}")

        return response

    def add_Exam(self, request):
        response = {"status": "fail"}
        try:
            info = request

            esame_nome = info["exam_name"].lower()  # Converti il nome dell'esame a minuscolo per il confronto
            esame_data = info["dates"]

            #crea dizionario per esame
            esame = {
                "nome": info["exam_name"],  # Mantieni il nome originale per la memorizzazione
                "data": [esame_data]
            }

            try:
                with open("esami.json", "r") as f:
                    esami = json.load(f)  # Carica i dati esistenti
            except FileNotFoundError:
                esami = []  # Se il file non esiste, crea un nuovo elenco di esami
            except json.JSONDecodeError:
                print("Errore nel decodificare il file JSON, creando un nuovo elenco di esami.")
                esami = []

            esame_trovato = False

            for e in esami:
                if e["nome"].lower() == esame_nome:
                    esame_trovato = True
                    if esame_data not in e["data"]:
                        e["data"].append(esame_data)  # Aggiungi la nuova data se non esiste
                        e["data"] = sorted(e["data"], key=lambda x: datetime.strptime(x, "%d-%m-%Y"))  # Ordina le date
                        response["status"] = "success"
                    break

            if not esame_trovato:
                esami.append(esame)  # Aggiungi un nuovo esame se non esiste
                response["status"] = "success"

            with open("esami.json", "w") as f:
                json.dump(esami, f, indent=2)  # Salva i dati aggiornati nel file JSON

        except Exception as e:
            print(f"Errore durante l'aggiunzione dell'esame: {e}")

        return response

    #metodo all'interno del quale vengono gestite tutte le tipologie di richieste effettuate dal client
    def process_request(self, request):
        try:
            if 'type' not in request:
                return {'error': "Request type is missing"}
            #login studente
            if request['type'] == 'login':
                print("richiesta login in verifica...\n")
                with open("studenti.json", 'r') as f:
                    users = json.load(f)  # Carica i dati degli studenti
                    response = {"status": "fail", "matricola": ""}
                    for user in users:
                        if user["username"] == request["username"] and user["psw"] == request["password"]:
                            print("Login Corretto!\n")
                            response["status"] = "success"
                            response["matricola"] = user["matricola"]
                            break 
                    return response
            #aggiunta esami
            elif request['type'] == "addExam":
                response = self.add_Exam(request)  # Processa la richiesta di aggiunta esame
                return response
            #prenotazioni esami
            elif request['type'] == "bookExam":
                response = self.book_Exam(request)  # Processa la richiesta di prenotazione esame
                return response

        except Exception as e:
            print(f"Errore in gestione response: {e}")

    def start(self):
        print("Starting Server...")
        while True:
            client_sock, client_address = self.server_socket.accept()  # Accetta connessioni dal client
            print(f"Accepted connection from {client_address}")  # Stampa l'indirizzo del client connesso
            client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock,))
            client_handler.start()  # Avvia un thread per gestire la connessione del client

if __name__ == '__main__':
    server = UniversityServer()  # Crea un'istanza del server
    server.start()  # Avvia il server
