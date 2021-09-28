# 필요 패키지 : pandas, selenium, openpyxl
# chromedriver chrome 버전에 맞게 설치

import time
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome("./chromedriver")

# 중고 명품 검색한 view 페이지 진입
driver.get("https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EC%A4%91%EA%B3%A0%EB%AA%85%ED%92%88")
time.sleep(2)

# 30개 블로그 url 리스트
blog_url_elements = driver.find_elements_by_css_selector("a.api_txt_lines.total_tit._cross_trigger")
blog_urls = [i.get_attribute('href') for i in blog_url_elements]

# error url
error_url_indexs = []

# 30개 블로그 본문 리스트
contents = []
for url in blog_urls:
    # 블로그 링크 진입
    driver.get(url)
    try:
        # 블로그일 때
        driver.switch_to.frame(driver.find_element_by_css_selector('iframe#mainFrame'))
    except:
        # 카페 - 로그인 창이 떠서 조회 불가 (검색으로 유입이 아니라 직접 url 유입이기 때문)
        # 마지막에 다시 접속
        error_url_indexs.append(blog_urls.index(url))
        # 순서대로 채워넣기 위해서 error 내용 넣기
        contents.append('error')
        continue

    # 본문 내용 가져오기
    content = driver.find_element_by_xpath('//div[@class="se-main-container"]').text
    content = content.replace("\n", " ")
    contents.append(content)

# 로그인 창 떴을 경우 삭제
while (len(driver.window_handles) > 1):
    # 열린 창 기준으로 선택
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()

# error 났던 링크 다시 접속하기 위한 코드
driver.switch_to.window(driver.window_handles[0])
driver.get("https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EC%A4%91%EA%B3%A0%EB%AA%85%ED%92%88")
time.sleep(1.5)
elements = driver.find_elements_by_xpath("//a[@class='api_txt_lines total_tit _cross_trigger']")

for error_url_index in error_url_indexs:
    driver.switch_to.window(driver.window_handles[0])
    elements[error_url_index].click()

    while (len(driver.window_handles) > 2):
        # 로그인 창 선택
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[1])
    try:
        # 카페
        driver.switch_to.frame(driver.find_element_by_css_selector('iframe#cafe_main'))
        time.sleep(0.5)
        content = driver.find_element_by_xpath('//div[@class="se-main-container"]').text
    except:
        # 네이버 포스트
        content = driver.find_element_by_xpath('//div[@class="se_component_wrap sect_dsc __se_component_area"]').text
    content = content.replace("\n", " ")
    # error 났던 index에 본문 채워넣기
    contents[error_url_index] = content
    # 검색 창으로 복귀
    driver.close()


# 엑셀 내보내기
data = {'content' : contents}
data = pd.DataFrame(data)
data.to_excel(excel_writer = 'blog_content.xlsx')
