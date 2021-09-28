from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver')

driver.get('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EC%8B%9C%EC%82%AC%2F%EA%B5%90%EC%96%91+%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8')
time.sleep(0.5)
driver.find_element_by_css_selector("a.sort_title._trigger_week").click()

check = driver.find_elements_by_css_selector("a._item")

for c in check:
    if "전체" in c.text:
        c.click()
    break

driver.find_element_by_css_selector("a.btn_apply._apply").click()

for page in range(2, 52):
    li = driver.find_elements_by_css_selector('div.item > dl > dt > a')

    for t in li:
        print(t.text)


    driver.find_element_by_css_selector("span.next").click()
    current = driver.find_element_by_css_selector('em._current').text
    total = driver.find_element_by_css_selector('em._total').text
    if current == total:
        break
    time.sleep(0.5)