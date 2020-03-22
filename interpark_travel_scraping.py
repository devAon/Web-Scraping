from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


main_url = 'http://tour.interpark.com/'
keyword = '스위스'

driver = webdriver.Chrome(executable_path = './chromedriver.exe')

driver.get(main_url)

driver.find_element_by_id('SearchGNBText').send_keys(keyword)
driver.find_element_by_css_selector('.search-btn').click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'oTravelBox'))
    )
except Exception as e:
    print('오류 발생', e)

driver.implicitly_wait(10)    
driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()

