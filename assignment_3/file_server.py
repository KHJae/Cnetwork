# file_server.py

import socket
import argparse
import os
import glob

def run_server(port, directory):
    host = '' ## 127.0.0.1 Loopback
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1) ## max 1 client
        conn, addr = s.accept()

        F_name = conn.recv(1024) # 전송할 파일 이름
        file_name = F_name.decode()
        path = "C://Users//khj40//Cnetwork//assignment_3//" + directory + "//" + file_name # 전송할 파일의 경로
        Gpath = directory + "/" + file_name # glob() 경로
        try :
                size = os.path.getsize(path) # 파일의 크기
                file_list = glob.glob(Gpath) # 해당 경로의 디렉토리 파일 목록
                print("file name : %s" % (file_list[0]))
                print("size : %d" % (size))
                with open(path, "rb") as f:
                        push_item = f.read(size) # 전송할 파일 읽기
                        conn.sendall(push_item) # 파일 전송
        except:
                print(">> [ %s 파일을 찾을 수 없습니다 ] <<" % (file_name))
        conn.close()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -d directory")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-d', help="file_directory", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p), directory=args.d)