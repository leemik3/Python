from selenium import webdriver
import openpyxl
import time
#컬럼 순서 변경, 팀명을 idx로 바꾸기
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['월','구단','경기합계'])

# 웹드라이버 켜기
driver = webdriver.Chrome("./chromedriver")

# 야구 경기 사이트 접속하기
driver.get("https://www.koreabaseball.com/History/Crowd/GraphDaily.aspx")

# 일정 검색 버튼 누르기

year_select = driver.find_element_by_css_selector("select#cphContents_cphContents_cphContents_ddlSeason")
for option in year_select.find_elements_by_tag_name('option'):
    if option.text == "2019": #2019년 입력
        option.click()
        break



away_select = driver.find_element_by_css_selector("select#cphContents_cphContents_cphContents_ddlHomeAway")
for option in away_select.find_elements_by_tag_name('option'):
    if option.text == "방문": #방문 입력
        option.click()
        break

for input_month in ["03월","04월","05월","06월","07월","08월","09월","10월","11월","12월"]:

    ##월 선택
    month_select = driver.find_element_by_css_selector("select#cphContents_cphContents_cphContents_ddlMonth")
    for option in month_select.find_elements_by_tag_name('option'):
        if option.text == str(input_month): #월 입력
            print(option)
            option.click()
            break
    ##구단 선택
    for team in ["두산","롯데","삼성","키움","한화","KIA","KT","LG","NC","SK"]:
        team_select = driver.find_element_by_css_selector("select#cphContents_cphContents_cphContents_ddlTeam")
        for option in team_select.find_elements_by_tag_name('option'):
            if option.text == str(team):  # 구단 입력
                option.click()
                break
        driver.find_element_by_css_selector("input#cphContents_cphContents_cphContents_btnSearch").click()


        # 검색 결과 수집하기

        ## 선택자 (컨테이너)
        ## 날짜, 시간, 경기 팀 2개, 점수, 구장
        time.sleep(1)

        plays = driver.find_elements_by_css_selector("span#cphContents_cphContents_cphContents_lblCrowdSum")[0].text
        print("2019년 %s 구단 : %s, 경기 합계 : %s" %(input_month, team, plays))

        sheet.append([input_month, team, plays])


wb.save('plays.csv')

#################################
'''
from selenium import webdriver
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['년','월','날짜','시간','팀1','팀2','점수1','점수2','장소','사유'])

# 웹드라이버 켜기
driver = webdriver.Chrome("./chromedriver")

# 야구 경기 사이트 접속하기
driver.get("https://www.koreabaseball.com/Schedule/Schedule.aspx")

# 일정 검색 버튼 누르기

for input_year in range(2020,2021,1):
    ##년도 선택
    year_select = driver.find_element_by_css_selector("select#ddlYear")
    for option in year_select.find_elements_by_tag_name('option'):
        if option.text == str(input_year): #년도 입력
            option.click()
            break

    for input_month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
        ##월 선택
        month_select = driver.find_element_by_css_selector("select#ddlMonth")
        for option in month_select.find_elements_by_tag_name('option'):
            print("0"+str(input_month))
            if option.text == input_month: #월 입력
                option.click()
                break

        # 검색 결과 수집하기

        ## 선택자 (컨테이너)
        ## 날짜, 시간, 경기 팀 2개, 점수, 구장
        container = driver.find_elements_by_css_selector("tbody tr")


        for c in container:
            try:
                date = c.find_element_by_css_selector("td.day").text
            except:
                pass

            try:
                time = c.find_element_by_css_selector("td.time b").text
            except:
                continue
            team1 = c.find_element_by_css_selector("td.play>span").text
            team2 = c.find_elements_by_css_selector("td.play>span")[1].text
            place = c.find_elements_by_css_selector("td")[-2].text
            try:
                score1 = c.find_elements_by_css_selector("td.play em span")[0].text
                score2 = c.find_elements_by_css_selector("td.play em span")[2].text
            except: #특정 사유로 경기 취소될 경우
                score1 = "-"
                score2 = "-"
                reason = c.find_elements_by_css_selector("td")[-1].text
                print("%s %s %s %s vs %s %s , %s %s" %(date, time, team1,score1,score2, team2, place, reason))
                sheet.append([input_year,input_month,date,time,team1,team2,score1,score2,place,reason])
                continue

            print("%s %s %s %s vs %s %s , %s" %(date, time, team1,score1,score2, team2, place))
            sheet.append([int(input_year),int(input_month.replace("0","")),date,time,team1,team2,int(score1),int(score2),place])


wb.save('baseball.csv')

'''