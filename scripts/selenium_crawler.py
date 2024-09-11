from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time

# 크롬 드라이버 경로를 정확히 입력하세요
chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)

# 크롬 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")  # 사용자 프로필 사용
chrome_options.add_argument("--profile-directory=Default")  # 기본 프로필 사용

# 크롬 브라우저 열기
driver = webdriver.Chrome(service=service, options=chrome_options)

# 노션 페이지 URL
notion_page_url = "https://www.notion.so/1c49f622006f410b9e1ccd2442150ba4"

# 노션 페이지 열기
driver.get(notion_page_url)

# 페이지가 잘 열렸는지 확인하고 10초간 대기
time.sleep(10)

# 브라우저 종료