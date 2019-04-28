import socket
import threading
import argparse


def socket_handler(conn):
    msg = conn.recv(1024)
    reverse_msg = msg.decode()[::-1]
    conn.sendall(reverse_msg.encode())
    conn.close()
    print(addr[0], ' : Closed')
  



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        print('Connected : ',addr[0], ' : ', addr[1])
        my_thread = threading.Thread(target = socket_handler, args = (conn,))
        my_thread.start() 
    server.close()