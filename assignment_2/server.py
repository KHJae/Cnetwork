# server.py

import socket
import argparse


def run_server(port=4000):
    host = '' ## 127.0.0.1 Loopback
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1) ## max 1 client
        conn, addr = s.accept()
        msg = conn.recv(1024)
        print(msg.decode())
        Reverse_msg = msg.decode()[::-1] # 문자 거꾸로 변환
        conn.sendall(Reverse_msg.encode())
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-s', help="string", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p))