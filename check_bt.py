import os
from tabnanny import check


#piscan을 자동화하기 위해 
os.system("sudo hciconfig hci0 piscan")

porcess_read = os.popen("ps -ef | grep bt_servo2.py | grep -v 'grep' ").readlines()
# ps -ef 명령어를 이용해서 현재 프로세스를 출력한 후, 그 중 run24h.py 문자열이 포함된 줄만 모은다.
# grep 명령어 자체도 프로세스에 나타나므로 grep -v를 이용해서 제외한다.
check_process = str(porcess_read)
# 문자열로 변환한다.

text_location  = check_process.find("bt_servo2.py")
# run24h.py가 몇번째 문자열인지 찾아낸다. 만약 문자열이 없으면, 즉 프로세스가 존재하지 않을 경우에는 -1을 반환한다.
if text_location == -1:
    print("process not found!")
    os.system("python3 bt_servo2.py &")
    # 해당 프로그램을 다시 실행한다. 백그라운드에서 실행할 경우 &기호를 붙인다.
    print("program restarted!")
else:
    print("process exits. Location is " , text_location)
