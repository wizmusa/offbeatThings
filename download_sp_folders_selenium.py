
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# --- 설정 (기존 스크립트와 동일) ---
SHAREPOINT_URL = 'https://COMPANY.sharepoint.com' # COMPANY: SharePoint URL 주소
SITE_PATH = '/sites/Site_name'  # Site_name: SharePoint site 이름
DOC_LIBRARY = 'Shared Documents' # Shared Documents: 문서 라이브러리 이름
FOLDERS_TO_DOWNLOAD = [
    'Folder_name_1', 'Folder_name_2',
    'Folder_name_3'
]
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver') # Chrome driver 필요 (https://developer.chrome.com/docs/chromedriver)

# --- 스크립트 본문 ---

def wait_for_downloads_to_complete(download_dir, timeout=900): # 15 minutes timeout
    start_time = time.time()
    # List of common temporary download extensions for Chrome, Firefox, Edge
    temp_extensions = ('.crdownload', '.part', '.tmp', '.download')
    
    print("      [정보] 다운로드 진행 중... 대기 중...", end='', flush=True) # Print once

    while True:
        # Check for timeout
        if time.time() - start_time > timeout:
            print("\n      [경고] 다운로드 완료 대기 시간 초과 ({timeout}초). 다음 폴더로 진행합니다.")
            return False

        # Get list of files in download directory
        files = os.listdir(download_dir)
        
        # Assume download is ongoing if any temporary file is present or if there's a zero-byte file
        download_in_progress = False
        for filename in files:
            filepath = os.path.join(download_dir, filename)
            if filename.endswith(temp_extensions) or (os.path.isfile(filepath) and os.path.getsize(filepath) == 0):
                download_in_progress = True
                break
        
        if not download_in_progress:
            # If no temporary files and no zero-byte files, assume download is complete
            print("\n      [정보] 모든 다운로드가 완료된 것으로 보입니다.")
            return True
        
        print(".", end='', flush=True) # Print dot on the same line
        time.sleep(60) # Check every 1 minute


def main():
    # 다운로드 폴더 생성
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Selenium WebDriver 설정
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DOWNLOAD_DIR}
    options.add_experimental_option("prefs", prefs)
    
    # 헤드리스 모드 비활성화 (마우스 오버 등을 정확히 보기 위함)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20) # 필요에 따라 대기 시간 조절

    try:
        # SharePoint 문서 라이브러리로 이동
        full_url = f"{SHAREPOINT_URL}{SITE_PATH}/{DOC_LIBRARY}"
        driver.get(full_url)
        driver.maximize_window() # 전체 화면으로 실행

        # 사용자가 수동으로 로그인하고 MFA를 완료할 때까지 대기
        print("-" * 50)
        print("브라우저가 열렸습니다. SharePoint에 로그인하고 MFA 인증을 완료해주세요.")
        print(f"로그인 후, 다운로드할 폴더들이 보이는 '{DOC_LIBRARY}' 페이지로 이동했는지 확인하세요.")
        input("로그인 및 페이지 이동이 완료되었으면 여기서 Enter 키를 누르세요...")
        print("-" * 50)

        # 다운로드할 폴더 목록에 있는 중복 항목 제거
        unique_folders = sorted(list(set(FOLDERS_TO_DOWNLOAD)))
        total_folders = len(unique_folders)

        for i, folder_name in enumerate(unique_folders):
            print(f"[{i+1}/{total_folders}] '{folder_name}' 폴더 다운로드 시도...")

            try:
                # 1. 폴더 이름이 title 속성에 정확히 일치하는 <span> 요소를 찾고,
                #    그 요소의 상위 div 중에서 role='row'인 것을 찾습니다.
                folder_row_xpath = f"//span[@title='{folder_name}']/ancestor::div[@role='row']"
                folder_row = wait.until(EC.presence_of_element_located((By.XPATH, folder_row_xpath)))

                # 2. 상호작용 전에 해당 요소가 보이도록 화면 중앙으로 스크롤합니다.
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", folder_row)
                time.sleep(1) # 스크롤 후 UI가 안정화될 시간을 줍니다.

                # 3. 찾은 'folder_row' 내부에서 '...' 메뉴 버튼을 찾아 JavaScript로 클릭합니다.
                more_button_xpath = ".//button[@data-automationid='moreActionsHeroField']"
                more_button = folder_row.find_element(By.XPATH, more_button_xpath)
                
                driver.execute_script("arguments[0].click();", more_button)
                print(f"  - '...' 메뉴 버튼을 JavaScript로 클릭했습니다.")
                time.sleep(1) # 메뉴가 열릴 때까지 대기

                # 4. 화면에 나타난 컨텍스트 메뉴에서 'Download' 버튼을 찾아 클릭합니다.
                time.sleep(1) # 메뉴 애니메이션 대기
                download_button_xpath = "//*[normalize-space()='Download']"
                download_button = wait.until(EC.visibility_of_element_located((By.XPATH, download_button_xpath)))

                # ActionChains를 사용하여 더 안정적인 클릭 시도
                ActionChains(driver).move_to_element(download_button).click().perform()
                print(f"  - 'Download' 메뉴 클릭. ZIP 파일 다운로드가 시작됩니다.")

                # 다운로드가 시작되고 완료될 때까지 충분히 대기합니다.
                print(f"      [정보] '{folder_name}' 폴더 다운로드 완료를 대기 중...")
                wait_for_downloads_to_complete(DOWNLOAD_DIR)
                print(f"  - [성공] '{folder_name}.zip' 다운로드가 시작되었으며 완료된 것으로 보입니다.")

            except TimeoutException:
                print(f"  - [실패] '{folder_name}' 폴더를 찾을 수 없거나 관련 메뉴(..., Download)가 시간 내에 나타나지 않았습니다.")
                print(f"      XPath가 SharePoint UI 구조와 일치하는지 확인이 필요할 수 있습니다.")
            except Exception as e:
                print(f"  - [오류] '{folder_name}' 폴더 처리 중 예기치 않은 오류 발생: {e}")
            
            print("-" * 20)

    finally:
        print("모든 작업이 완료되었습니다. 30초 후에 브라우저를 닫습니다.")
        time.sleep(30)
        driver.quit()

if __name__ == '__main__':
    main()
