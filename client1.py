import socket
import sys
import DES
import server

g = 71
n = 7
a = 5

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 4598
    

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")
    message = input(" -> ")

    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        if soc.recv(5120).decode("utf8") == "-":
            pass        # null operation

        message = input(" -> ")

    soc.send(b'--quit--')

def get_key():
    print("KEY:", (g**a)%n)
    return (g**a)%n

def diffie(key, sharedkey):
    (n, g, user) = kdc.recv(1024).decode("utf8").split("|")
    n = int(n)
    g = int(g)

    #Waiting for Server to send it's first part of DH. Converts it into an int to be used later
    k1 = int(key.recv(1024).decode("utf8").rstrip())
    
    #Performing the first step of DH for the client now, and sending it to the kdc
    client_1 = (g ** key) % n
    key.send(str(client_firstStep).encode())

    sharedKey = (kdc_firstStep ** PRIVATE_KEY) % PUBLIC_P

    print("Finished Diffie-Hellman.")
    return bin(sharedKey)[2:].zfill(10), MY_ID
if __name__ == "__main__":
    main()