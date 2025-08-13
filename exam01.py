# harman2 폴더 내
# server 폴더 내
# exam01.py

# request : client -> server
# response : server -> client

# python server
# 1) flask : 마이크로 웹 프레임워크 (12000 line)
# 2) Django : 모든 기능이 포함!! (flask보다 10 ~ 20배 무겁다)

# 가상환경 변경
# 우측 하단 3.9.13 혹은 가상환경 이름을 클릭
# ctrl + shift + p -> 인터프리터 검색 -> 인터프리터 선택
# 한글 설치 안했으면, interpreter -> select interpreter
from flask import Flask # route 경로, run 서버 실행
from flask import render_template # html load
from flask import request # 사용자가 보낸 정보
from flask import redirect # 
from flask import make_response

# aws.py 안에 detect_ 함수만 사용하고 싶은 경우
from aws import detect_labels_local_file
from aws import compare_faces as cf

# 파일명 보안처리 라이브러리
from werkzeug.utils import secure_filename

import os
# static 폴더가 없으면 생성
if not os.path.exists("static"):
    os.mkdir("static")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compare", methods=["POST"])
def compare_faces():
    # 1. compare로 오는 file1, file2를 받아서 static 폴더에 저장
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]
        #파일 이름을 sucure_filename으로 보안
        file1_name = secure_filename(file1.filename)
        file2_name = secure_filename(file2.filename)
        # file을 static 폴더에 저장하고
        file1.save("static/" + file1_name)
        file2.save("static/" + file2_name)
    # 2. secure_filename 사용해서 aws.py 얼굴 비교 aws 코드 업로드
        r = cf("static/" + file1_name, "static/" + file2_name)
    # 3. aws.py 안 함수를 불러와서 exam01
    return r


@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method == "POST":
            # get -> args[key], post -> form[key]
            hidden = request.form["hidden"]
            return f"비밀 정보 : {hidden}"
    except:
        return "데이터 전송 실패"
    

@app.route("/detect", methods=["POST"])
def detect_label():
    # flask 보안 규칙상 file 이름을 secure 처리 해야 한다
    if request.method == "POST":
        file = request.files["file"]
        
        # file을 static 폴더에 저장하고
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        # 해당 경로를 detect_ 함수에 전달
        r = detect_labels_local_file("static/" + file_name)        

    return r


@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        # 페이지가 이동하더라도
        # 정보를 남겨서 사용
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id == "munho" and login_pw == "1234":
            response = make_response(redirect("/login/success"))
            response.set_cookie("user", login_id)
            return response
        else:
            # 페이지 이동
            return redirect("/")


@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
