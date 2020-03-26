from selenium import webdriver as wd
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

import time
from Tour import TourInfo

from DbMgr import DBHelper as Db
db = Db()

main_url = 'http://tour.interpark.com/' 
keyword  = '스위스'
tour_list = []

driver = wd.Chrome(executable_path='chromedriver.exe')
driver.get(main_url)

driver.find_element_by_id('SearchGNBText').send_keys(keyword)
driver.find_element_by_css_selector('button.search-btn').click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located( (By.CLASS_NAME, 'oTravelBox') )
    )
except Exception as e:
    print( '오류 발생', e)

driver.implicitly_wait( 10 )
driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()

for page in range(1, 2):
    try:
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print("%s 페이지 이동" % page)
        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        for li in boxItems:
            print( '썸네임', li.find_element_by_css_selector('img').get_attribute('src') )
            print( '링크', li.find_element_by_css_selector('a').get_attribute('onclick') )
            print( '상품명', li.find_element_by_css_selector('h5.proTit').text )
            print( '코멘트', li.find_element_by_css_selector('.proSub').text )
            print( '가격',   li.find_element_by_css_selector('.proPrice').text )
            area = ''
            for info in li.find_elements_by_css_selector('.info-row .proInfo'):
                print(  info.text )
            print('='*100)

            # obj = TourInfo(title, price, area, link, img, contents)
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text,
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src'),
                li.find_element_by_css_selector('.proSub').text 
            )
            tour_list.append( obj )

    except Exception as e1:
        print( '오류', e1 )

print(tour_list, len(tour_list))
for tour in tour_list:
    print(type(tour))
    arr = tour.link.split(',')
    if arr:
        link = arr[0].replace('searchModule.OnClickDetail(','')
        detail_url = link[1:-1]
        driver.get( detail_url )
        time.sleep(1)
        soup = bs (driver.page_source, 'html.parser')
        data = soup.select('.tip-cover')
        print( type(data), len(data), type(data[0].contents)  )

        content_final = ''
        for c in data[0].contents:
            content_final += str(c)
        
        import re
        content_final   = re.sub("'", '"', content_final)
        content_final   = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)

        print( content_final )

        db.db_insertCrawlingData(
            tour.title,
            tour.price[:-1],
            tour.area.replace('출발 가능 기간 : ',''),
            content_final,
            keyword
        )


#종료
driver.close()
driver.quit()
import sys
sys.exit()