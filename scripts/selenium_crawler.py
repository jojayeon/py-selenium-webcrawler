from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")  # 사용자 프로필 사용
chrome_options.add_argument("--profile-directory=Default")  # 기본 프로필 사용

# 크롬 드라이버 열기
driver = webdriver.Chrome(service=service, options=chrome_options)

# 노션 페이지로 이동
notion_page_url = "https://www.notion.so/kongukjae/c05dce133c984e2c8e72bbb89063cb40?v=9cce7377e99c4e629eb4940b802403d6"
driver.get(notion_page_url)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 20)  # 타임아웃을 20초로 늘리기

def get_parent_element():
    parent_selector = "#notion-app > div > div:nth-child(1) > div > div:nth-child(2) > main > div > div > div:nth-child(5) > div > div > div > div:nth-child(3) > div:nth-child(3)"
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, parent_selector)))

def get_child_elements(parent_element):
    child_selector = "div > div.notion-table-view-row > div > div:nth-child(3) > div > div"
    return parent_element.find_elements(By.CSS_SELECTOR, child_selector)

# 부모 요소를 가져오고 자식 요소들을 검색
parent_element = get_parent_element()
child_elements = get_child_elements(parent_element)

# 각 자식 요소에 대해 마우스 오버 및 클릭 시도
for index in range(len(child_elements)):
    try:
        child = child_elements[index]
        
        actions = ActionChains(driver)
        actions.move_to_element(child).perform()
        
        # 열기 버튼 클릭
        open_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='페이지로 열기']")))
        open_button.click()
        
        # 새 페이지가 로드될 때까지 대기
        wait.until(EC.url_changes(notion_page_url))
        
        # 현재 페이지 URL 추출
        current_url = driver.current_url
        print(f"수집한 URL (요소 {index + 1}):", current_url)
        
        # 원래 페이지로 돌아가기
        driver.back()
        
        # 원래 페이지가 완전히 로드되기까지 대기
        parent_element = get_parent_element()
        child_elements = get_child_elements(parent_element)
        
        # 다시 마우스 오버를 위한 요소 찾기
        child = child_elements[index]

    except Exception as e:
        print(f"오류 발생 (요소 {index + 1}):", e)

# 브라우저 닫기
driver.quit()
