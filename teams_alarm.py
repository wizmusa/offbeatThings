import signal
import time
import pymsteams

# MS Teams Webhook URL
WEBHOOK_URL = "https://hanwha.webhook.office.com/webhookb2/20acc195-0bad-4658-b033-7f921e0ed5ef@0f7b4e1c-344e-4923-aaf0-6fca9e6700c8/IncomingWebhook/8ebcccd3229c405c81fcce75dffd71e9/208b10a3-c124-4555-b31b-ae3356afc0fc"

# 타임아웃 시간 (초)
TIMEOUT = 10

def read_file(file_path):
    # 파일 읽기 작업 수행
    with open(file_path, 'r') as f:
        content = f.read()
    return content

def timeout_handler(signum, frame):
    # 타임아웃 발생 시 호출되는 함수
    send_teams_notification(f"File reading took longer than {TIMEOUT} seconds.")
    # print(f"File reading took longer than {TIMEOUT} seconds.")
    raise TimeoutError("File reading timed out.")

# MS Teams 알림 전송 함수
def send_teams_notification(message):
    myTeamsMessage = pymsteams.connectorcard(WEBHOOK_URL)
    myTeamsMessage.text(message)
    myTeamsMessage.send()

# 메인 함수
def main():
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']  # 읽을 파일 경로 리스트
    
    # 타임아웃 핸들러 등록
    signal.signal(signal.SIGALRM, timeout_handler)
    
    for file_path in file_paths:
        # 타임아웃 설정
        signal.alarm(TIMEOUT)
        
        try:
            time.sleep(15)
            #content = read_file(file_path)
            print(f"File '{file_path}' read successfully.")
            # 파일 내용 처리 코드 추가
        except TimeoutError:
            print(f"File '{file_path}' reading timed out.")
        
        # 타임아웃 해제
        signal.alarm(0)

if __name__ == "__main__":
    main()