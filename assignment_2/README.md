2주차 과제 : 클라이언트가 보낸 문자열을 거꾸로 전송해주는 서버 구현
===
#### 김현재(2015040013), 신중수(2015040023)

* client.py
    * 서버 아이피 : -i
    * 포트 번호 : -p
* server.py
    * 문자열 : -s
    * 포트 번호 : -p

.socket() : 소켓 객체 생성|.bind() : IP와 포트번호 연결|.listen() : 연결 수신 대기 상태
----|----|----
.accept() : 연결 수락|.recv() : 데이터 송신|.sendall() : 데이터 수신
* 실행 결과

![result](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_2/result.PNG)

