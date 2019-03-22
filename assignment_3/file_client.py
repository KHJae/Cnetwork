# file_client.py

import socket
import argparse
import os

def run(host, port, Fname):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        print("file name : %s " % (Fname))
        s.sendall(Fname.encode())
        path = "C://Users//khj40//Cnetwork//assignment_3//" + Fname  # 전송받을 파일의 경로 
        pull_item = s.recv(1024) # 전송받은 파일
        with open(Fname, "wb") as f:
                f.write(pull_item) # 파일 저장
        if os.path.getsize(path) == 0:
                os.remove(Fname) # 생성된 파일 삭제
                print("파일 요청 실패")
        else:
                print("전송받은 파일의 size : %d" % (os.path.getsize(path))) #전송 받은 파일의 크기
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -f Fname")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-i', help="host_name", required=True)
    parser.add_argument('-f', help="file_name", required=True)
    
    args = parser.parse_args()
    run(host=args.i, port=int(args.p), Fname=args.f)