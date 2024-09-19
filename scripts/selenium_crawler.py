import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains  # ActionChains 임포트 추가
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from konlpy.tag import Okt

chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default")

# Chrome 드라이버 열기
driver = webdriver.Chrome(service=service, options=chrome_options)

# 노션 페이지 URL
notion_page_url = "https://www.notion.so/kongukjae/RockCoders-de66453690144c53a0dc9d065a43e5f0"
driver.get(notion_page_url)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 20)
okt = Okt()  # Okt 객체 생성

def get_parent_element():
    parent_selector = "#notion-app > div > div:nth-child(1) > div > div:nth-child(2) > main > div > div > div:nth-child(5) > div > div > div > div:nth-child(3) > div:nth-child(3)"
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, parent_selector)))

def get_child_elements(parent_element):
    child_selector = "div > div.notion-table-view-row > div > div:nth-child(3) > div > div"
    return parent_element.find_elements(By.CSS_SELECTOR, child_selector)

# URL 수집하기
collected_urls = []
parent_element = get_parent_element()
child_elements = get_child_elements(parent_element)

for index in range(len(child_elements)):
    try:
        child = child_elements[index]
        
        actions = ActionChains(driver)
        actions.move_to_element(child).perform()
        
        open_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='페이지로 열기']")))
        open_button.click()
        
        wait.until(EC.url_changes(notion_page_url))
        
        current_url = driver.current_url
        collected_urls.append(current_url)
        print(f"수집한 URL (요소 {index + 1}):", current_url)
        
        driver.back()
        parent_element = get_parent_element()
        child_elements = get_child_elements(parent_element)
        
        child = child_elements[index]

    except Exception as e:
        print(f"오류 발생 (요소 {index + 1}):", e)

# 수집한 URL로 이동하여 데이터 추출하고 JSON으로 저장하기
data_collection = []  # 데이터를 저장할 리스트

for url in collected_urls:
    try:
        driver.get(url)
        
        # main 태그가 로드될 때까지 대기
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))  
        
        # main 태그 내 모든 데이터 가져오기
        main_element = driver.find_element(By.TAG_NAME, "main")
        all_data = main_element.text  # 모든 텍스트 가져오기
        
        # Okt를 사용하여 형태소 분석
        tokens = okt.morphs(all_data)  # 형태소로 분리
        
        # 데이터 구조화
        data_collection.append({
            "url": url,
            "data": all_data,
            "tokens": tokens  # 형태소 리스트 추가
        })
        
        print(f"{url}에서 추출한 데이터:\n", all_data)
        print(f"{url}의 형태소:\n", tokens)  # 형태소 출력
        
    except Exception as e:
        print(f"{url}에서 데이터 추출 중 오류 발생:", e)

# JSON 파일로 저장
with open("collected_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data_collection, json_file, ensure_ascii=False, indent=4)

# 브라우저 닫기
driver.quit()