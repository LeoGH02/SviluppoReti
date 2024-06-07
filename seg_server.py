import sys
import tkinter
import socket
import threading
import json


def get_users():
    with open("users.json","r") as f:
        return json.load(f)

users = get_users()



def ricevi_comandi(conn):
    while True:
        data = conn.recv(4096).decode('utf-8')
        if not data:
            break
        elif data == "esami":
            messaggio="esami:ASD\nElim"
        else:
            messaggio="non ok"
        conn.send(messaggio.encode('utf-8'))
    conn.close()





def create_server_socket(indirizzo, backlog=1):
    try:
        #creiamo il socket per il server
        s=socket.socket()
        #gli associamo un indirizzo e una porta
        s.bind(indirizzo)
        #facciamo in modo che il server ascolti
        s.listen(backlog)
        print(f"Server in Ascolto su {indirizzo}")
    except socket.error as errore:
        print(f"C'è stato un errore durante la creazione del server socket\n.Codice errore:{errore}")
        #proviamo a farlo riconettere
        create_server_socket(indirizzo,backlog=1)
        return
    
    while True:
        conn,indirizzo_client = s.accept()
        #accept restituisce una tupla, il primo valore è la connesione in se, il secondo è l'ip del client
        #uso il modulo threading per creare un thread che mi permetterà l'invio e la ricezione di dati da quella connessione
        print(f"Connessione stabilita con {indirizzo_client}")
        data = conn.recv(4096).decode('utf-8')
        credentials = json.loads(data)

        response={"status":"fail"}
        for user in users:
            if user["username"] == credentials["username"] and user["psw"] == credentials["password"]:
                response["status"]="success"
                break
    
        conn.send(json.dumps(response).encode('utf-8'))
        conn.close()
    




if __name__ == "__main__":
    create_server_socket(("",15000))





























