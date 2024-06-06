#Creazione Client SOCKET

#1-Creazione del socket         | socket.socket()
#2-Connessione al server        | connect(indirizzo)
#3-Invio richiesta al server    | send()
#4-Ricezione Risposta Server    | recv()




import socket
import sys
import tkinter


def invia_comandi(s):
    while True:
        comando = input("->")
        if comando == "ESC":
            print("Sto uscendo")
            s.close()
            sys.exit()
        else:
            s.send(comando.encode())
            #metodo rcv: come primo parametro ha un sizebuffer, ovvero la grandezza dei pacchetti che vogliamo inviare
            data = s.recv(4096)
            print(str(data,"utf-8"))



def connect_to_seg(indirizzo):
    try:
        s = socket.socket() #creiamo il soccket, di defualt avrà comunicazione con indirizzi IPV4 e protocollo TCP
        s.connect(indirizzo)
        print(f"Connessione avvenuta con successo.\nIndirizzo{indirizzo}")
    except socket.error as errore:
        print(f"Errore: Connessione non stabilita\nCodice Errore:{errore}")
        sys.exit()
    invia_comandi(s)



if __name__ == '__main__':
    connect_to_seg(("192.168.1.13",15000))











