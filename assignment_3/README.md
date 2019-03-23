3주차 과제 : 클라이언트가 요청한 파일을 전송해주는 서버 구현
===
#### 김현재(2015040013), 신중수(2015040023)

* file_server.py
    * 포트 번호 : -p
    * 파일 디렉토리 : -d
> $python file_server.py -p 포트번호 -d "파일디렉토리"
* file_client.py
    * 서버 아이피 : -i
    * 포트 번호 : -p
    * 파일 이름 : -f
> $python file_client.py -i 서버아이피 -p 포트번호 -f "파일이름"
  
* 실행 결과

===== 요청한 파일이 존재할 경우 =====
   
> ![result](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_3/result.PNG)

===== 요청한 파일이 존재하지 않은 경우 =====

> ![result2](https://raw.githubusercontent.com/KHJae/Cnetwork/master/assignment_3/result2.PNG)

