import socket
import sys
import traceback
import client1
import client2
import random
from threading import Thread

g = 71
n = 7

def main():
    start_server()


def start_server():
    host = "127.0.0.1"
    port = 4598         # arbitrary non-privileged port
    conns = {}
    
    k_a = -1000
    k_b = -1000

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")
    
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])

        if connection.getpeername() not in conns:
            conns[connection.getpeername()] = [len(conns)+1]
            print(conns[connection.getpeername()])
            if conns[connection.getpeername()]==[1]:
                k_a = client1.get_key()
                print("Received key", k_a, "from client1")
            else:
                k_b = client2.get_key()
                print("Received key", k_b, "from client2")

        print("Connected with " + ip + ":" + port + " as client", conns[connection.getpeername()])

        try:
            Thread(target=client_thread, args=(connection, ip, port, conns)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()

def diffieHellman(connection, user):
    # make random key
    key = ''
    for i in range(10):
        key += str(random.randint(0,1))
    
    key = int(key,2)

    # send n and g to client
    connection.send('{:}|{:}|{:}'.format(n,g,user).encode())

    k1 = (g ** key) % n
    connection.send(str(k1).encode())

    #Waiting for Server to send it's first part of DH. Converts it into an int to be used later
    client_1 = int(connection.recv(1024).decode("utf8").rstrip())

    sharedKey = (client_1 ** key) % n
    print("Finished Diffie-Hellman with User {:}.\n".format(user))
    return bin(sharedKey)[2:].zfill(10)



def client_thread(connection, ip, port, conns, max_buffer_size = 5120):
    is_active = True

    user = conns[connection.getpeername()][0]
    print("Diffie Hellman Key Exchange with client"+str(user))
    # call diffie hellman 
    diffieHellman(connection, user)

    while is_active:
        client_input = receive_input(connection, conns, max_buffer_size)

        if "--QUIT--" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))


def receive_input(connection, conns, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    user = conns[connection.getpeername()]
    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input, user)

    return result


def process_input(input_str, user):
    name = "client"+str(user) 
    print("Processing the input received from", str(name))

    return str(input_str)

if __name__ == "__main__":
    main()