import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# Chrome 드라이버 경로
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
notion_page_url = "https://www.notion.so/64fa68fc31464a6e95570b77403cb0d1?v=a38b4aba61904e519bdad3f703777e94"
driver.get(notion_page_url)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#notion-app")))

# 페이지 로드 후 대기 (5초)
time.sleep(5)

# 제외할 단어 목록
excluded_words = {
    "시작 전", "계산", "새로 만들기", "즐겨찾기", "개인 페이지",
    "5시간 전 편집", "모든 페이지", "7시간 전 편집", "혼자 공부하는데 데이터 분석 with 파이썬", "댓글의 코드",
    "TOP 관리", "노드 및 NPM 설치 (1)", "규칙 설정 방법 및 규칙 설정 (1)", "7.11 작업중 모르는 것", "크롤링 test 파일",
    "서버 업데이트 서버 관리 (1)", "SSH 접속을 위한 PuTTY 설치 (1)", "ACL 비활성화 활성화 차이가 뭐지? (1)", "8시간 전 편집",
    "각 서버 실행 (1)", "바벨", "표기법 코드", "혼자 공부하는데이터 분석 with 파이썬"
}

# 데이터 가져오기
collected_data = set()  # 중복을 제거하기 위해 집합 사용
scrollable_div = driver.find_element(By.CSS_SELECTOR, "#notion-app > div > div:nth-child(1) > div > div:nth-child(2) > main > div > div")

previous_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

# 스크롤을 통해 화면에 보이는 데이터 가져오기
while True:
    try:
        # 현재 보이는 영역에서 span 태그 선택
        visible_elements = driver.find_elements(By.CSS_SELECTOR, "span")

        # 데이터 출력, 빈 값 및 제외할 단어 필터링
        for element in visible_elements:
            text = element.text.strip()
            if text and text not in excluded_words and "편집" not in text:  # "편집"이 없는 경우만 추가
                collected_data.add(text)  # 집합에 추가

        # 스크롤 내리기
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
        time.sleep(3)  # 페이지가 로드될 시간을 기다림

        # 새로운 높이를 가져와서 이전 높이와 비교
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == previous_height:  # 더 이상 스크롤할 수 없으면 종료
            break
        previous_height = new_height

    except Exception as e:
        print("Error while fetching elements:", e)
        break

# 날짜를 월과 일로 추출하는 함수
def extract_month_day(text):
    parts = text.split(" ")
    for part in parts:
        try:
            date_obj = datetime.strptime(part[:10], "%Y-%m-%d")
            return (date_obj.month, date_obj.day)  # 월, 일을 튜플로 반환
        except ValueError:
            continue
    return (0, 0)  # 날짜가 없으면 (0, 0) 반환

# 월, 일 순서로 정렬
sorted_data = sorted(collected_data, key=extract_month_day)

# JSON 파일로 저장
with open("name.json", "w", encoding="utf-8") as json_file:
    json.dump(sorted_data, json_file, ensure_ascii=False, indent=4)

# 브라우저 닫기
driver.quit()

print("데이터가 name.json 파일에 저장되었습니다.")
