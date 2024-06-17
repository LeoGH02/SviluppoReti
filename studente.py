import json # Importa il modulo JSON per lavorare con dati JSON
import socket # Importa il modulo socket per le connessioni di rete
import tkinter as tk # Importa il modulo tkinter per creare interfacce grafiche
from tkinter import messagebox # Importa il modulo messagebox per le finestre di dialogo
from functools import partial # Importa partial per creare funzioni parziali

# Implementazione della connessione STUDENTE-SEGRETERIA-UNIVERSITÀ
# Implementazione della funzione login 

class StudentClient:

    def __init__(self, host = "localhost", port = 10001):
        # Inizializzazione del client
        self.host = host
        self.port = port
        #creazione socket: AF_INET specifica la tipologia di indirizzi (in questo caso IPV4), sock_Stream indica il protocollo TCP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un socket TCP

    def connect_to_server(self):
        # Connessione al server
        try:
            self.client_socket.connect((self.host,self.port))
            print("Connessione Stabilita con Server Segreteria")
        except socket.error as errore:
            print(f"Connessione non riuscita\nErrore:{errore}") 
            exit()   
    
    def send_login_request(self,username,password):
        # Invia la richiesta di login al server
        credentials = {"username":username, "password":password,"type":"login"} # Dati delle credenziali in formato dizionario
        self.client_socket.send(json.dumps(credentials).encode('utf-8')) # Invia i dati al server codificati in JSON

        response = json.loads(self.client_socket.recv(4096).decode('utf8')) # Riceve e decodifica la risposta del server
        return response
    

    def send_exam_table_request(self):
        # Invia la richiesta per visualizzare gli esami e le date ad essi associati
        request = {"type":"viewExams"} # Tipo di richiesta
        self.client_socket.send(json.dumps(request).encode('utf-8')) # Invia la richiesta al server
        response = json.loads(self.client_socket.recv(4096).decode('utf-8')) # Riceve e decodifica la risposta del server
        return response
    
    def send_exam_booking_request(self,esame,matricola,data):
        # Invia la richiesta per prenotare un esame
        booking_data = {"matricola":matricola,"esame":esame,"data":data,"type":"bookExam"} # Dati di prenotazione
        self.client_socket.send(json.dumps(booking_data).encode('utf-8')) # Invia i dati al server
        response = json.loads(self.client_socket.recv(4096).decode('utf-8')) # Riceve e decodifica la risposta del server
        return response

    
    def disconnect_from_server(self):
        # Disconnessione dal server
        self.client_socket.close()
        print("Connessione con il server chiusa")

        
            
        



class StudentGui:

    def __init__(self, student_client):
        self.student_client = student_client
        #crea finestra principale 
        self.root = tk.Tk()
        self.root.title("Login") #assegna titolo alla finestra
        self.root.geometry("250x250")#assegna dimensione alla finestra
        self.root.resizable(False, False)#questo metodo esclude il ridimensionamento della feinstra

        # Configura le righe e le colonne per espandersi
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Creazione e posizionamento dei widget
        self.user_label = tk.Label(self.root, text="Username")
        self.user_label.grid(row=0, column=0, padx=10, pady=1, sticky="n")

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=0, padx=10, pady=1, sticky="n")

        self.psw_label = tk.Label(self.root, text="Password")
        self.psw_label.grid(row=2, column=0, padx=10, pady=1, sticky="n")

        self.psw_entry = tk.Entry(self.root, show="*")
        self.psw_entry.grid(row=3, column=0, padx=10, pady=1, sticky="n")

        self.login_btn = tk.Button(self.root, text="Login", command=self.send_login_request)
        self.login_btn.grid(row=4, column=0, padx=10, pady=1, sticky="n")

        # Numero di matricola dello studente, inizializzato più avanti nel codice
        self.matricola = ""




    def create_user_window(self,username,student_number):
        # Nasconde la finestra del login
        self.root.withdraw()
        # Crea finestra secondaria che mostra gli esami
        user_window = tk.Toplevel(self.root)
        user_window.title("Esami Disponibili")

        first_label = tk.Label(user_window,text=f"Ciao {username} {student_number}! Cosa vuoi fare?")     
        first_label.grid(row=0,column=0,pady=(0,5))  
        #bottone per visualizzare gli esami
        view_ex_btn = tk.Button(user_window,text="Visualizzi Esami",command=self.view_Exam_table)
        view_ex_btn.grid(row=1,column=0,pady=(0,5),sticky="w")

        # Funzione annidata per gestire uscita e disconnessione dall'interfaccia
        def close_userRoot_window():
            user_window.destroy()
            self.student_client.disconnect_from_server()
            self.root.destroy()


        exit_btn = tk.Button(user_window, text="Esci", command=close_userRoot_window)
        exit_btn.grid(row=2,column=0,pady=10,sticky="w")


    #questo è un metodo che inserisce all'interno di una finestra secondaria tutti gli esami disponibili
    def view_Exam_table(self):
        # Visualizza la tabella degli esami
        esami = self.student_client.send_exam_table_request()
        exam_window = tk.Toplevel()
        exam_window.title("Esami")

        for i,esame in enumerate(esami):
            esa = tk.Label(exam_window,text=esame["nome"]).grid(row=i,column=0,pady=(0,10),sticky="w")
            see_dates_btn = tk.Button(exam_window,text="Vedi Date",
                                      command=partial(self.show_dates,esame["nome"],esame["data"]))
            see_dates_btn.grid(row=i, column=1,padx=10)

    #questo metodo fa la stessa operazione del precedente soltanto mostrando le date
    def show_dates(self, nome_esame, date_esame):
        # Visualizza le date degli esami
        date_window = tk.Toplevel()
        date_window.title("Date")

        # Visualizza il nome dell'esame
        tk.Label(date_window, text=nome_esame).grid(row=0, column=0, sticky="w")

        # Visualizza le date degli esami con i pulsanti
        for i, data in enumerate(date_esame):
            tk.Label(date_window, text=data).grid(row=i+1, column=0, sticky="w")  # Adjust row to start from 1
            prenota_esame_btn = tk.Button(date_window, text="Prenota",
                                          command=partial(self.book_exam,nome_esame,self.matricola,data))
            prenota_esame_btn.grid(row=i+1, column=1, padx=10, pady=10)

    #metodo di prenotazione dell'esame nel quale viene gestito solo l'esito di quest'utlima
    def book_exam(self,esame,matricola,data):
        # Prenota un esame
        response = self.student_client.send_exam_booking_request(esame,matricola,data)
        if response["status"] == "success":
            messagebox.showinfo("Successo",f"Prenotazione effettuata con Successo\n Numero Prenotazione {response['booking_number']}")
        else:
            messagebox.showerror("Errore","Prenotazione non Effettuata")

    #metodo di login che gestisce l'esito di quest'ultimo
    def send_login_request(self):
        # Invia la richiesta di login
        username = self.username_entry.get()
        password = self.psw_entry.get()
        response = self.student_client.send_login_request(username,password)
        # Effettua controllo della response ottenuta dal server
        if response["status"] == "success":
            messagebox.showinfo("Successo","Login avvenuto con successo")
            self.matricola = response["matricola"]
            self.create_user_window(username,self.matricola)
        else:
            messagebox.showerror("Errore", "username o password errati")


    def run(self):
        # Avvia il loop principale dell'interfaccia grafica
        self.root.mainloop()


if __name__ == "__main__":
    # Inizializzazione del client e dell'interfaccia grafica
    student_client = StudentClient()
    #si connette al server della segreteria tramite il metodo connect_to_server
    student_client.connect_to_server()
    #avvia l'interfaccia grafica
    gui = StudentGui(student_client)
    gui.run()
