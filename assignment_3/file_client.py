# file_client.py

import socket
import argparse
import os

def run(host, port, Fname):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        PATH = "C://Users//khj40//Cnetwork//assignment_3//" + Fname  # 전송받을 파일의 경로
        print("file name : %s " % (Fname))
        s.sendall(Fname.encode()) # [1]
        msg = s.recv(1).decode() # 파일의 존재 여부 [2]
        if msg == "Y" :
                Fsize = s.recv(1024).decode() # 전송받은 파일의 크기 [3] 
                s.sendall("OK".encode()) # [4]
                pull_item = s.recv(int(Fsize)) # 파일의 사이즈만큼 서버로 부터 파일 수신 [5]
                with open(Fname, "wb") as f:
                        f.write(pull_item) # 파일 저장
                print("file size : %d" % (os.path.getsize(PATH))) #전송 받은 파일의 크기        
        else:
                print("fail")
        
                
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -f Fname")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-i', help="host_name", required=True)
    parser.add_argument('-f', help="file_name", required=True)
    
    args = parser.parse_args()
    run(host=args.i, port=int(args.p), Fname=args.f)