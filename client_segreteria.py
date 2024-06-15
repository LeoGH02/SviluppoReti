import socket  # Importa il modulo socket per le comunicazioni di rete
import json  # Importa il modulo json per serializzare e deserializzare i dati in formato JSON
import tkinter as tk  # Importa il modulo tkinter per creare l'interfaccia grafica
from tkinter import messagebox  # Importa messagebox da tkinter per mostrare finestre di dialogo
from tkcalendar import Calendar  # Importa Calendar da tkcalendar per mostrare un widget calendario
from tkinter import simpledialog  # Importa simpledialog da tkinter per richiedere input all'utente

#poter aggiungere solamente le date se l'esame è già presente nel file
#aggiungere funzioni che manipolano le stringhe in caso in cui l'utente inserisce lo stesso nome di esame ma con maiuscole e minuscole differenti


class SecretaryClient:
    def __init__(self, server_host='localhost', server_port=10000):
        # Inizializza il client della segreteria con l'host e la porta del server
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP

    def connect_to_server(self):
        # Tenta di connettersi al server; in caso di errore, stampa un messaggio e termina il programma
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print("Connected to the University Server.")
        except ConnectionRefusedError:
            print("Failed to connect to the University Server.")
            exit()

    def add_exam(self, exam_name, date):
        # Invia una richiesta al server per aggiungere un nuovo esame con nome e data specificati
        request = { 'exam_name': exam_name, 'dates': date,'type': 'addExam'}
        self.client_socket.sendall(json.dumps(request).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(response)

    def close_connection(self):
        # Chiude la connessione con il server
        self.client_socket.close()



class SecretaryGUI:
    def __init__(self, secretary_client):
        # Inizializza l'interfaccia grafica della segreteria con un client della segreteria
        self.secretary_client = secretary_client
        self.root = tk.Tk()  # Crea la finestra principale
        self.root.title("Secretary Interface")  # Imposta il titolo della finestra
        self.root.geometry("600x600")

        # Crea e imballa i widget per l'input del nome dell'esame
        tk.Label(self.root, text="Exam Name:").pack()
        self.exam_name_entry = tk.Entry(self.root)
        self.exam_name_entry.pack()

        # Crea e imballa i widget per l'input della data dell'esame
        tk.Label(self.root, text="Exam Date:").pack()
        self.exam_date_entry = tk.Entry(self.root, state='readonly')
        self.exam_date_entry.pack()

        # Crea e imballa il bottone per mostrare il calendario e selezionare una data
        tk.Button(self.root, text="Select Date", command=self.show_calendar).pack()
        # Crea e imballa il bottone per aggiungere un esame
        tk.Button(self.root, text="Add Exam", command=self.add_exam).pack()


    def show_calendar(self):
        # Mostra il widget calendario per selezionare una data
        top = tk.Toplevel(self.root)  # Crea una nuova finestra di dialogo
        cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy')  # Crea il calendario
        cal.pack(pady=20)  # Imballa il calendario nella finestra di dialogo

        def on_date_select():
            # Funzione chiamata quando una data è selezionata
            date = cal.get_date()  # Ottiene la data selezionata
            self.exam_date_entry.config(state=tk.NORMAL)  # Rende scrivibile l'entry della data
            self.exam_date_entry.delete(0, tk.END)  # Cancella il contenuto attuale
            self.exam_date_entry.insert(0, date)  # Inserisce la data selezionata
            self.exam_date_entry.config(state='readonly')  # Rimette l'entry in stato readonly
            top.destroy()  # Chiude la finestra di dialogo

        tk.Button(top, text="Select", command=on_date_select).pack()  # Crea e imballa il bottone per selezionare la data

    def add_exam(self):
        # Invia una richiesta al server per aggiungere un nuovo esame
        exam_name = self.exam_name_entry.get()  # Ottiene il nome dell'esame dall'entry
        exam_date = self.exam_date_entry.get()  # Ottiene la data dell'esame dall'entry

        # Controlla se la data è vuota
        if not exam_date.strip():
            messagebox.showerror("Error", "The exam date cannot be empty.")  # Mostra un messaggio di errore
            return  # Interrompe l'esecuzione del metodo

        # Procede con l'invio della richiesta al server se la data non è vuota
        response = self.secretary_client.add_exam(exam_name, exam_date)  # Invia la richiesta e ottiene la risposta

        if response["status"] == "success":
            messagebox.showinfo("Fatto","Esame aggiunto correttamente")
        else:
            messagebox.showerror("Errore","Esame non Aggiunto")

    def run(self):
        # Avvia l'interfaccia grafica
        self.root.mainloop()  # Entra nel loop principale di Tkinter

if __name__ == "__main__":
    secretary_client = SecretaryClient()  # Crea un'istanza del SecretaryClient
    secretary_client.connect_to_server()  # Connette il SecretaryClient al server dell'Uni
    gui = SecretaryGUI(secretary_client)  # Crea l'interfaccia grafica passando il SecretaryClient
    gui.run()  # Avvia l'interfaccia grafica

























































