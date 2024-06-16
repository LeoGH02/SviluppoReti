import json
import socket
import threading
from datetime import datetime


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

    import json

    def get_exams_data(self):
        try:
            with open("esami.json", "r") as f:
                data = json.load(f)
                if data is not None:
                    # data è già un oggetto Python (una lista nel tuo caso)
                    # Continua con il trattamento dei dati JSON qui
                    for exam in data:
                        print(f"Esame: {exam['nome']}, Data: {exam['data']}")
                        return data
                else:
                    print("Dati non disponibili o vuoti")
        except FileNotFoundError:
            print("File non trovato")
        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare JSON: {e}")



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
                    prenotazioni = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                prenotazioni = []

            prenotazione_trovata = False

            # Verifica se la prenotazione associata a quel numero di matricola è già presente
            for p in prenotazioni:
                if (p["matricola"] == prenotazione["matricola"] and 
                    p["esame"] == prenotazione["esame"] and 
                    p["data"] == prenotazione["data"]):
                    prenotazione_trovata = True
                    break  # Esce dal ciclo una volta trovata la prenotazione

            # Dobbiamo restituire il numero progressivo per la prenotazione dello studente
            count_prenotazioni = sum(1 for p in prenotazioni if p["esame"] == prenotazione["esame"] and p["data"] == prenotazione["data"])
            response["booking_number"] = count_prenotazioni + 1

            # La nuova prenotazione viene prima accodata ai dizionari già presenti all'interno del file
            if not prenotazione_trovata: 
                prenotazioni.append(prenotazione)
                # Dopodiché il file viene sovrascritto con le nuove informazioni
                with open("prenotazioni.json", 'w') as f:
                    json.dump(prenotazioni, f, indent=2)
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

            esame = {
                "nome": info["exam_name"],  # Mantieni il nome originale per la memorizzazione
                "data": [esame_data]
            }

            try:
                # Carica i dati esistenti, se il file esiste e non è vuoto
                with open("esami.json", "r") as f:
                    esami = json.load(f)
            except FileNotFoundError:
                # Se il file non esiste, verrà creato quando scriveremo
                pass
            except json.JSONDecodeError:
                print("Errore nel decodificare il file JSON, creando un nuovo elenco di esami.")
            
            esame_trovato = False
            
            # Verifica se l'esame esiste già
            for e in esami:
                if e["nome"].lower() == esame_nome:
                    esame_trovato = True
                    if esame_data not in e["data"]:
                        e["data"].append(esame_data)
                        # Ordina le date
                        e["data"] = sorted(e["data"], key=lambda x: datetime.strptime(x, "%d-%m-%Y"))
                        response["status"] = "success"
                    break
            
            # Se l'esame non è stato trovato, aggiungilo alla lista
            if not esame_trovato:
                esami.append(esame)
                response["status"] = "success"
            
            # Scrivi nel file JSON
            with open("esami.json", "w") as f:
                json.dump(esami, f, indent=2)
            
        except Exception as e:
            print(f"Errore durante l'aggiunzione dell'esame: {e}")
        
        return response


    
    def process_request(self,request):
        try:
            if 'type' not in request:
                return {'error':"Request type is missing"}
            
            if request['type'] == 'login':
                print("richiesta login in verifica...\n")
                with open("studenti.json",'r')as f:
                    users = json.load(f)
                    response = {"status": "fail","matricola":""}
                    for user in users:
                        if user["username"] == request["username"] and user["psw"] == request["password"]:
                            print("Login Corretto!\n")
                            response["status"] = "success"
                            response["matricola"] = user["matricola"]
                            break 
                    return response
                
            elif request['type'] == "addExam":
                response = self.add_Exam(request)
                return response
            
            elif request['type'] == "bookExam":
                response = self.book_Exam(request)
                return response

        except Exception as e:
            print(f"Errore in gestione response: {e}")        

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












