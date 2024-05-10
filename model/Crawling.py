from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://eminwon.gangseo.seoul.kr/emwp/gov/mogaha/ntis/web/emwp/cns/action/EmwpCnslWebAction.do?method=selectCnslWebPage&menu_id=EMWPCnslWebInqL&jndinm=EmwpCnslWebEJB&methodnm=selectCnslWebPage&context=NTIS')

while True:
    time.sleep(3)  # 페이지 로딩 대기 시간을 1초에서 3초로 늘립니다.
    elements = driver.find_elements(By.CLASS_NAME, "td-list")
    
    if len(elements) == 0:  # 'elements' 리스트가 비어있는 경우, 다시 로딩을 시도합니다.
        continue

    with open('output.txt', 'a', encoding='utf-8') as f:
        for i in range(len(elements)):
            f.write(elements[i].text + '\n')

    navi_elements = driver.find_elements(By.CLASS_NAME, "navi")

    if len(navi_elements) < 14:
        break

    navi_elements[13].click()

time.sleep(100000)
driver.quit()