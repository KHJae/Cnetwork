# 5주차 과제 : Threading 모듈을 사용해 다수의 client의 요청을 받을 수 있는 서버 작성
## 김현재 (2015040013), 신중수 (2015040023)
* 서버는 클라이언트가 전송한 문자열을 뒤집어서 클라이언트에게 전송해준다.
* 클라이언트는 서버 연결 후 input() 함수를 사용해 사용자로부터 문자열을 입력 받는다.
* python thread_server.py -p 8888
* python thread_client.py -p 8888 -i 127.0.0.1



구분|Blocking|Non-blocking 
:----|:----|:----
Synchronous : 동기|Read/Write | Read/Write(Polling)
Asynchronous : 비동기 |I/O Multiplexing(select/Poll)| Asynchronous I/O

## thread.join() : 한 스레드가 처리될때까지 다른 스레드를 대기 하는 기능 
> ### Result : 총 3개의 클라이언트로 실습, 위 클라이언트부터 차례대로 서버접속 후 2,3번째 클라이언트 문자열 전송 
![server_client(before input)](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_5/server_client(before%20input).png)

> ### Result : 1번 클라이언트의 요청이 처리가 안되어 2,3번 클라 요청 대기 -> 1번 클라 문자열 전송 후 2, 3번 클라의 문자열도 전송
![server_client(after input)](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_5/server_client(after%20input).png)

> ### Result : thread.join() 미사용, 총 3개의 클라이언트로 실습, 서버는 클라이언트가 전송한 문자열을 뒤집어 전송
![not_use_join()](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_5/not_use_join().png)


