import socket
import sys
import server

g = 71
n = 7
b = 12

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 4559
    

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
    return (g**b)%n

if __name__ == "__main__":
    main()