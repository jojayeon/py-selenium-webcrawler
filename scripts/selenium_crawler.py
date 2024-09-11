from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

# 크롬 드라이버 경로를 정확히 입력하세요
chrome_driver_path = r"C:\Users\Administrator\chromedriver-win64\chromedriver.exe"

# 서비스 객체 생성
service = ChromeService(executable_path=chrome_driver_path)

# 크롬 브라우저 열기
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기 (예: 구글)
driver.get("https://www.google.com")

# 페이지가 잘 열렸는지 확인하고 5초간 대기
driver.implicitly_wait(5)

# 브라우저 종료
driver.quit()
