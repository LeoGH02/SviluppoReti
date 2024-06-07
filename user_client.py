#Creazione Client SOCKET

#1-Creazione del socket         | socket.socket()
#2-Connessione al server        | connect(indirizzo)
#3-Invio richiesta al server    | send()
#4-Ricezione Risposta Server    | recv()




import socket
import sys
import tkinter as tk
import json
from tkinter import messagebox


#def invia_comandi(s):
#    while True:
#        comando = input("->")
#        if comando == "ESC":
#            print("Sto uscendo")
#            s.close()
#            sys.exit()
#        else:
#            s.send(comando.encode())
            #metodo rcv: come primo parametro ha un sizebuffer, ovvero la grandezza dei pacchetti che vogliamo inviare
#            data = s.recv(4096)
#            print(str(data,"utf-8"))








def connect_to_seg(indirizzo):
    try:
        s = socket.socket() #creiamo il socket, di defualt avrà comunicazione con indirizzi IPV4 e protocollo TCP
        s.connect(indirizzo)
        print(f"Connessione avvenuta con successo.\nIndirizzo{indirizzo}")
    except socket.error as errore:
        print(f"Errore: Connessione non stabilita\nCodice Errore:{errore}")
        sys.exit()
    return s



def send_login_request(username,password):
 
    #crea il socket
    client_socket = connect_to_seg(("192.168.1.13",15000))
    #ci prendiamo le informazioni e le mettiamo in un formato dizionario, adatto per la libreria json
    credentials={"username":username,"password":password}
    #mandiamo le informazioni al sever
    client_socket.send(json.dumps(credentials).encode('utf-8'))

    #questa è la response che riceveremo dal server
    response = client_socket.recv(4096).decode('utf-8')
    #chiudiamo la socket
    client_socket.close()

    #restituiamo il risultato
    return json.loads(response)





def user_interface(username):
    usr_inter = tk.Toplevel()
    usr_inter.title("Interfaccia")

    # Configura il peso delle righe e delle colonne per adattarsi al contenuto
    usr_inter.grid_rowconfigure(0, weight=1)
    usr_inter.grid_columnconfigure(0, weight=1)

    win_label = tk.Label(usr_inter, text=f"Ciao {username}! Cosa vuoi fare?", font=("Helvetica",16))
    win_label.grid(row=0, column=0, sticky="n", padx=10, pady=10)  # Allinea il label in alto a sinistra con padding

    view_ex_btn = tk.Button(usr_inter, text="Prenota un appello")
    view_ex_btn.grid(row=1, column=0, sticky="n", padx=10, pady=(0, 10))  # Allinea il bottone sotto al label con padding solo sotto

    #funzione annidata per chiudere la finestra corrente
    def close_window():
        usr_inter.destroy()

    exit_btn = tk.Button(usr_inter, text="Esci", command=close_window)
    exit_btn.grid(row=2, column=0, sticky="n", padx=10, pady=(0,10))

    


    




def login():
    username = usr_entry.get()
    password = psw_entry.get()

    response = send_login_request(username,password)

    if response['status'] == 'success':
        messagebox.showinfo("Successo", "Login avvenuto con successo!")
        root.withdraw()
        user_interface(username)
    else:
        messagebox.showerror("Errore", "Username o password errati")

    







#creazione gui per utente
root = tk.Tk()
root.title("Login")
root.geometry("250x150")

usr_label=tk.Label(root,text="username").grid(row=0,column=0)
usr_entry = tk.Entry(root)
usr_entry.grid(row=1,column=0)

psw_label = tk.Label(root,text="password").grid(row=2,column=0)
psw_entry = tk.Entry(root, show="*")
psw_entry.grid(row=3,column=0)

login_btn = tk.Button(text="Login",command=login).grid(row=4, columnspan=2)



if __name__ == '__main__':
    #connect_to_seg(("192.168.1.13",15000))
    root.mainloop()











