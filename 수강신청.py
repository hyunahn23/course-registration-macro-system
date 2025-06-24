import os
import sys
import schedule
import time
from tkinter import *
import tkinter.messagebox
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 정해진 날짜를 지나가면 더 이상 실행 불가
present = datetime.now()
specified_date = datetime(2023, 2, 24)
if present > specified_date:
    exit()

# 현재 라이브러리 주소 불러오는 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def manual():
    # 설명서 파일 열고 내용 쓰기
    with open(resource_path("manual\\manual.txt"), "w") as manual_txt:
        manual_txt.write("""<-- 사용법 -->
이 프로그램은 정식 프로그램입니다.
정식 프로그램은 실행 버튼을 클릭시
수강신청 3초전까지 대기하다가 3초전이 되면 실행 됩니다.

1. 학번과 비밀번호 입력
2. 로그인
3. 크롬이 켜지면 '실행' 버튼 클릭

===로그인이 안될시 직접 로그인 해주면 됌===

*** 주의 사항 ***
Chrome 버전을 104로 맞춰주세요
USER가 아닐 시 로그인 후 브라우저가
강제 종료됩니다.
USER 등록은 관리자에게 부탁하세요.

수강신청 당일 날이 지나면 더 이상
프로그램 사용이 불가능합니다.

<--제작자-->
LEERO
""")

    # manual.txt 실행하기
    os.startfile(resource_path("manual\\manual.txt"))

browser = None
url = 'https://sugang.hongik.ac.kr/cn1000.jsp'

# 유저가 맞는지 확인하는 함수
def user():
    # top 클래스의 문자열을 가져옴
    global browser
    name = browser.find_element(By.CLASS_NAME, "top")
    name_text = name.text

    # 가져온 값이 '이근님 환영합니다'이므로 이름만 따로 저장
    # print(name_text[:name_text.index("님")])
    name_text = name_text[:name_text.index("님")]
    print(name_text)
    # user.txt 파일을 열어서 유저가 맞는지 확인
    with open(resource_path("user\\user.txt"), "r", encoding = 'utf-8') as user_name:
        lines = user_name.read().split()
        if name_text in lines:
            pass
        else:
            browser.quit()
            exit()

def login(event):
    browser_login()

def browser_login():
    # id 입력이 안되면 경고 메세지
    if input_id.get() == '':
        tkinter.messagebox.showinfo("아이디 입력", "아이디(학번)를 입력하세요.")
        return
    # pw 입력이 안되면 경고 메세지
    elif input_pw.get() == '':
        tkinter.messagebox.showinfo("비밀번호 입력", "비밀번호를 입력하세요.")
        return

    global browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(resource_path("chromedriver\\chromedriver.exe"), options=options) # ./chromedriver.exe  

    # 수강신청 사이트 이동
    browser.get(url)
    browser.maximize_window()

    # id, pw 입력
    browser.find_element(By.NAME, "p_userid").send_keys(input_id.get()) # id 입력
    browser.find_element(By.NAME, "p_passwd").send_keys(input_pw.get()) # pw 입력

    # 로그인 버튼 누르기
    browser.find_element(By.CLASS_NAME, "buttonA").click()

    

# period를 멈추는 함수
def next_job():
    schedule.cancel_job(job1)
    run()
    schedule.cancel_job(job2)

# 새로고침 눌러주는 함수
def time_rerefresh():
    browser.refresh()

# 시간에 따라 실행 함수
def period():
    # 브라우저가 실행되지 않으면 로그인 메세지 출력
    if browser == None:
        tkinter.messagebox.showinfo("로그인", "로그인을 해주세요")
        return
    
    # user 검사
    user()

    global job1, job2
    # 30초마다 새로고침
    job1 = schedule.every(30).seconds.do(time_rerefresh)
    # 정해진 시간이 되면 stop함수 실행
    job2 = schedule.every().day.at("08:59:56").do(next_job)

    while True:
        # job 변수를 반복 실행
        schedule.run_pending()

# 실행 함수
def run():
    # 담은 과목 수강신청 반복 클릭
    global browser
    while True:
        # 브라우저 그냥 종료 시 run함수 종료
        try:
            browser.find_element(By.LINK_TEXT, '- 담은 과목 수강신청하기').click()
        except:
            browser.quit()
            browser = None
            return
        # alert 가 나오면 확인 누르고 안나오면 반복문 빠져나감
        try:
            alert = browser.switch_to.alert
            alert.accept()
        except:
            break
    # 다음화면 나올때까지 대기
    elem = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'buttonA')))
    elem[2].click()

    return

def exit_window():
    if browser == None:
        root.destroy()
    else:
        root.destroy()
        browser.quit()
    

root = Tk()
root.title("수강신청")

frame_login = Frame(root)
frame_login.pack(padx=5, pady=5)

# id 레이블
label1 = Label(frame_login, text="아이디")
label1.grid(row=0, column=0)

input_id = StringVar()

# id 엔트리 칸 만들기
login_id = Entry(frame_login, width=30, textvariable=input_id)
login_id.grid(row=0, column=1)
login_id.focus()

# pw 레이블
label1 = Label(frame_login, text="패스워드")
label1.grid(row=1, column=0)

input_pw = StringVar()

# pw 엔트리 칸 만들기
login_pw = Entry(frame_login, width=30, show="*", textvariable=input_pw)
login_pw.grid(row=1, column=1)

# 버튼 레이블
frame_btn = Frame(root)
frame_btn.pack(fill="x", padx=5, pady=5)

# 설명서 버튼
manual_btn = Button(frame_btn, padx=10, pady=5, text="설명서", command=manual)
manual_btn.pack(side="left")

# 실행 버튼
run_btn = Button(frame_btn, padx=10, pady=5, text="실행", command=period)
run_btn.pack(side = "right")

# 로그인 버튼
login_btn = Button(frame_btn, padx=10, pady=5, text="Login", command=browser_login)
login_btn.pack()
# Enter키와 연동
root.bind('<Return>', login)

# 윈도우창 X 누를 시 행동
root.protocol('WM_DELETE_WINDOW', exit_window)

# tkinter 아이콘
root.iconbitmap(resource_path("test.ico"))

root.mainloop()