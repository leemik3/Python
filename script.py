# SW 리더십 세미나 출결 Script
# venv tf24
# 이미경

'''
1) 학생 구분 : 학번_이름
2) 이 로그에는 없을 수 있지만, 학생 별로 overlap되는 시간들이 있을 수 있어요. overlap되는 시간은 제거되도록 해야 해요.
3) 참여 누적 시간이 전체 수업시간의 85% 이상이 되면 출석 / 그 이외에는 결석
4) 수업 시작 후 5분 이후에 들어오면 지각이에요.

- 출결 사유 기재하기
- 수업 일찍 끝나면 일찍 끝난 시간 기준으로 하기
- 결과물 엑셀로 만들기
- 매주 출석 공지로
- claim을 1주일 동안 받기, 지나면 수정 불가
- 사캠 3개 다 신청 - 신청 완료
- 기말과제
- 3번 대체 공휴일 - 녹화
- 매주 수업 시간 전에 동창회관 우체국 아래층? 202호? : 김경주 선생님, 연사님께 드릴 주차권/참여록/등등 받아오기
- 컴퓨터공학 ewha.ac.kr 계정 받아서 로그인 - 공동 호스트 - 박사 언니 여쭤보기 - 없다 하심
- 첫 2주는 엑셀은 보여주되 다 출석으로 인정
- 연사님 강연은 신공 152호
'''

'''
파일명, 수업 시작 시간, 끝나는 시간, 저장할 파일명 확인
'''

import pandas as pd
import re
from datetime import datetime, date

pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 10)


# 이름 형식 전처리 함수
def remove(string):
    index = string.find(" (")
    if index != -1:
        string = string[:index]
    return string


def to_time(string):
    return string.time()


def to_datetime(string):
    return datetime.combine(date.min, string)


# overlap 되는 시간 처리 - df 받아서 overlap 되는 시간 반환 (나중에 빼야 되는 시간임)
def get_overlap(df):
    in_list = [to_datetime(x) for x in df['in_time']]
    out_list = [to_datetime(x) for x in df['out_time']]
    overlap_time = 0
    for i in range(len(in_list) - 1):
        if out_list[i] > in_list[i + 1]:
            # a 케이스
            if out_list[i+1] < out_list[i]:
                overlap_time += int((out_list[i+1] - in_list[i+1]).seconds/60)
            # b 케이스
            elif out_list[i+1] >= out_list[i]:
                overlap_time += int((out_list[i] - in_list[i+1]).seconds/60)
    return overlap_time


# 수업 시작 시간, 수업 끝나는 시간 - 형식 datetime.time, 강의 시간 - 형식 int 미리 설정
start_time = "2021-06-15 17:00:00"
start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').time()
end_time = "2021-06-15 17:20:00"
end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').time()
lecture_time = int((to_datetime(end_time)-to_datetime(start_time)).seconds/60)  # 강의 시간


def max_time(in_time):
    global start_time
    return max(start_time, in_time)


def min_time(out_time):
    global end_time
    return min(end_time, out_time)


# 기록 시간, 강의 시간에 따라 출결 상태 반환 함수
def check_attendance(record_time):
    global lecture_time
    if record_time < lecture_time*0.85:
        return 2 # 결석
    else:
        return 0 # 출석


# 들어온 시간에 따라 지각 체크
def check_late(in_time):
    global start_time
    if int((to_datetime(in_time)-to_datetime(start_time)).seconds/60) > 5:
        return 1 # 지각
    else:
        return 0


# 출/결/지 숫자 받아서 최종 출결 반환
def get_result(df):
    result = max(df['attendance'], df['late'])
    if result == 2:
        return "결석"
    elif result == 1:
        return "지각"
    elif result == 0:
        return "출석"
    else:
        return "error"

# email 암호화
def encrypt(text):
    index = text.find("@")
    return text[:2]+"*"*(index-3)+text[index-1:]

# 계정 상태
def account_able(email):
    index = email.find("@")
    if email[index+1:] == 'ewhain.net':
        return '정상'
    else:
        return '인정 불가'

# 학번 추출
def accnum(text):
    index = text.find("_")
    return int(text[:index])

def acc_result(df):
    if df['계정 상태'] == '인정 불가':
        return '결석'
    else:
        return df['result']

# 4번째 행부터 읽어오기
file = pd.read_csv("0906_participants_86048204364.csv", header=3)
file.columns = ['name', 'email', 'in_time', 'out_time', 'remain_time', 'guest', 'record_YN']


# 분반 출석부 불러오기 (대학, 학과, 학번, 이름만)
list_0 = pd.read_csv("분반0.csv").iloc[:, [1, 2, 3, 4]]
list_1 = pd.read_csv("분반1.csv").iloc[:, [1, 2, 3, 4]]
list_2 = pd.read_csv("분반2.csv").iloc[:, [1, 2, 3, 4]]


# 정규표현식으로 [8글자_이름] 형식인 사람들과 아닌 사람들 데이터프레임 각각 생성
file_1 = file.loc[file.name.str.contains(r'(\w{7,8}_\w*)')]  # 정규표현식에 해당하는 이름들만 새로운 데이터프레임
file_1 = file_1.iloc[:, [0, 1, 2, 3]]  # 이름, 들어온시간, 나간시간 컬럼만 남기기
file_1['name'] = file_1['name'].map(remove)  # 이름 중에 '1871057_현오주 (오주 현)' 와 같은 값이 있어서 처리
file_1 = file_1.sort_values(by=['name', 'in_time'], ascending=[True, True])  # 이름 다음으로 들어오는 시간 순 정렬
file_2 = file.loc[file.name.str.contains(r'(\w{7,8}_\w*)') == False]  # 정규표현식에 해당하지 않는 이름들
file_2 = file_2.iloc[:, [0, 1, 2, 3]]

# 들어온/나간 시간을 datetime 형식으로 바꿈
file_1['in_time'] = pd.to_datetime(file_1['in_time'])
file_1['out_time'] = pd.to_datetime(file_1['out_time'])
file_1['in_time'] = file_1['in_time'].map(to_time)
file_1['out_time'] = file_1['out_time'].map(to_time)


# 입장 시간이 수업 시작 시간보다 빠를 경우 수업 시작 시간으로 변경
file_1['in_time'] = file_1['in_time'].map(max_time)
# 퇴장 시간 - 수업 시작 시간보다 빠를 경우 삭제
drop_index = file_1[file_1['out_time'] <= start_time].index  # 삭제할 인덱스
file_1 = file_1.drop(drop_index)
# 퇴장 시간 - 수업 끝나는 시간보다 느릴 경우 수업 끝나는 시간으로 변경
file_1['out_time'] = file_1['out_time'].map(min_time)
# 입장 시간이 수업 끝나는 시간보다 느릴 경우 삭제
drop_index = file_1[file_1['in_time'] >= end_time].index  # 삭제할 인덱스
file_1 = file_1.drop(drop_index)


# 행별 기록 시간 집계
file_1['record_time'] = file_1['out_time'].map(to_datetime) - file_1['in_time'].map(to_datetime)
file_1['record_time'] = file_1['record_time'].map(lambda x: int(x.seconds/60))


# overlap 되는 시간 계산
overlap = pd.DataFrame(file_1.groupby('name')['in_time'].apply(list))
overlap['out_time'] = file_1.groupby('name')['out_time'].apply(list)


overlap['overlaptime'] = overlap.apply(get_overlap, axis=1)
#overlap['overlaptime'] = overlap['overlaptime'].map(lambda x: 0)  #overlap 되는 시간 오류 있을 경우 그냥 0으로 초기화


# 학생 별 기록 시간 합하고, overlap 시간 빼기
result_1 = pd.DataFrame(file_1['record_time'].groupby(file_1['name']).sum())
result_1['학번'] = result_1.index.map(accnum)
result_1['account'] = file_1['email'].unique()
result_1['account'] = result_1['account'].map(encrypt)
result_1['계정 상태'] = result_1['account'].map(account_able)
result_1['in_time'] = file_1['in_time'].groupby(file_1['name']).min()
result_1['pure_record_time'] = result_1['record_time'] - overlap['overlaptime']
result_1['최소 인정 시간'] = pd.Series([int(lecture_time*0.85) for i in range(len(result_1))], index=result_1.index)
result_1 = result_1.drop(['record_time'], axis=1)

# 출석 0 지각 1 결석 2 : 최종 출결
result_1['attendance'] = result_1['pure_record_time'].map(check_attendance)
result_1['late'] = result_1['in_time'].map(check_late)
result_1['result'] = result_1.apply(get_result, axis=1)
result_1 = result_1.drop(['attendance', 'late'], axis=1)
result_1['프로필 이름'] = result_1.index
result_1 = result_1.reset_index(drop=True)

# 계정 상태에 따라 결석 처리
result_1['result'] = result_1.apply(acc_result, axis=1)


# 비정상출결
file_2['email'] = file_2['email'].map(encrypt)

file_2['in_time'] = pd.to_datetime(file_2['in_time'])
file_2['out_time'] = pd.to_datetime(file_2['out_time'])
file_2['in_time'] = file_2['in_time'].map(to_time)
file_2['out_time'] = file_2['out_time'].map(to_time)

# 입장 시간이 수업 시작 시간보다 빠를 경우 수업 시작 시간으로 변경
file_2['in_time'] = file_2['in_time'].map(max_time)
# 퇴장 시간 - 수업 시작 시간보다 빠를 경우 삭제
drop_index = file_2[file_2['out_time'] <= start_time].index  # 삭제할 인덱스
file_2 = file_2.drop(drop_index)
# 퇴장 시간 - 수업 끝나는 시간보다 느릴 경우 수업 끝나는 시간으로 변경
file_2['out_time'] = file_2['out_time'].map(min_time)
# 입장 시간이 수업 끝나는 시간보다 느릴 경우 삭제
drop_index = file_2[file_2['in_time'] >= end_time].index  # 삭제할 인덱스
file_2 = file_2.drop(drop_index)

file_2['record_time'] = file_2['out_time'].map(to_datetime) - file_2['in_time'].map(to_datetime)
file_2['record_time'] = file_2['record_time'].map(lambda x: int(x.seconds/60))


# 3개 분반
list_0 = pd.merge(list_0, result_1, how='left', on='학번')
list_1 = pd.merge(list_1, result_1, how='left', on='학번')
list_2 = pd.merge(list_2, result_1, how='left', on='학번')

list_0['result'] = list_0['result'].fillna('결석')
list_1['result'] = list_1['result'].fillna('결석')
list_2['result'] = list_2['result'].fillna('결석')


list_0.rename(columns={'account':'사용자 계정', 'in_time':'입장 시간', 'pure_record_time':'기록 시간', 'result':'출결 결과'})
list_1.rename(columns={'account':'사용자 계정', 'in_time':'입장 시간', 'pure_record_time':'기록 시간', 'result':'출결 결과'})
list_2.rename(columns={'account':'사용자 계정', 'in_time':'입장 시간', 'pure_record_time':'기록 시간', 'result':'출결 결과'})

list_0.to_excel("tess.xlsx")
'''

file_2.to_excel('0906_비정상출결.xlsx')
result_1.to_excel("0906.xlsx")



file = 원본 출결 파일
file_1 = 정규표현식 이름에 해당하는 데이터
file_2 = 정규표현식 이름에 해당 않는 데이터
overlap = 강의 들어온 시간 나간 시간 겹치는 경우
result_1 = 최종 출결 결과 데이터

'''
