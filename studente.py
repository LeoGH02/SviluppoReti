import json
import socket
import sys
import threading
import tkinter as tk
from tkinter import messagebox

#implementare connessione STUDENTE-SEGRETERIA-UNIVERSITA
#implementare funzione login 

class StudentClient:

    def __init__(self, host = "localhost", port = 10001):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host,self.port))
            print("Connessioen Stabilita con Server Segreteria")
        except socket.error as errore:
            print(f"Connessione non riuscita\nErrore:{errore}") 
            exit()   
    
    def send_login_request(self,username,password):
        #immagazzino i dati all'interno di un dizionario credenziali
        credentials = {"username":username, "password":password,"type":"login"}
        #mando queste credenziali al server della segreteria
        self.client_socket.send(json.dumps(credentials).encode('utf-8'))
        #a seconda della risposta ricevuta l'utente riceverà una notifica di conferma o di errore tramite messagebox
        response = json.loads(self.client_socket.recv(4096).decode('utf8'))
        return response
    
    def send_exam_table_request(self):
        #dico al server della segreteria che voglio solo ottenere i dati per visualizzare gli esami
        request = {"type":"viewExams"}
        #mando la richiesta al server
        self.client_socket.send(json.dumps(request).encode('utf-8'))
        #i dati ottenuti corrispondo agli esami presenti i quali sono gestiti altrove
        response = json.loads(self.client_socket.recv(4096).decode('utf-8'))
        return response
    
    def disconnect_from_server(self):
        self.client_socket.close()
        print("Connessione con il server chiusa")

        
            
        



class StudentGui:

    def __init__(self, student_client):
        self.student_client = student_client
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("250x250")
        self.root.resizable(False, False)

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




    def create_user_window(self,username):
        #nascondi la finestra del login
        self.root.withdraw()
        #crea finestra che mostra gli esami
        user_window = tk.Toplevel(self.root)
        user_window.title("Esami Disponibili")

        first_label = tk.Label(user_window,text=f"Ciao {username}! Cosa vuoi fare?")     
        first_label.grid(row=0,column=0,pady=(0,5))  

        view_ex_btn = tk.Button(user_window,text="Visualizzi Esami")
        view_ex_btn.grid(row=1,column=0,pady=(0,5),sticky="w")

        #funzione annidata per gestire uscita e disconnessione dall'interfaccia
        def close_userRoot_window():
            user_window.destroy()
            self.student_client.disconnect_from_server()
            self.root.destroy()


        exit_btn = tk.Button(user_window, text="Esci", command=close_userRoot_window)
        exit_btn.grid(row=2,column=0,pady=10,sticky="w")


    def view_Exam_table(self):
        response = self.student_client.send_exam_table_request()


    def send_login_request(self):
        username = self.username_entry.get()
        password = self.psw_entry.get()
        response = self.student_client.send_login_request(username,password)
        #effettua controllo della response ottenuta dal server
        if response["status"] == "success":
            messagebox.showinfo("Successo","Login avvenuto con successo")
            self.create_user_window(username)
        else:
            messagebox.showerror("Errore", "username o password errati")



    def run(self):
        self.root.mainloop()




if __name__ == "__main__":
    student_client = StudentClient()
    student_client.connect_to_server()
    gui = StudentGui(student_client)
    gui.run()






























