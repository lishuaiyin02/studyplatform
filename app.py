# coding: utf-8
import docker
import os
from werkzeug.utils import secure_filename   # 获取上传文件的文件名

import random  #生成随机数解决iframe问题
from config import Config

from flask import Flask
from flask import render_template, url_for, redirect
from flask import request, session

import requests
from requests.auth import HTTPBasicAuth
import json

from form import LoginForm, RegisterForm
from model import User
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

app = Flask(__name__)  # type: Flask

UPLOAD_FOLDER = r'static\materials'   # 上传路径
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','mp4','html'])   # 允许上传的文件类型
# app = Flask(__name__)  # type: Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):   # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    if '_user_id' in session:
        session['user_ip'] = request.remote_addr
        user_id = session['_user_id']
        if User.get(user_id):
            session['user_name'] = User.get(user_id).username
    return render_template('homepage.html', username=session['user_name'])


# 登入登出
# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

app.config["SECRET_KEY"] = "12345678"
# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

# 登入
@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        config=Config()
        print("url_token",config.url_tokens)
        url = config.url_tokens
        username = form.username.data
        password = form.password.data
        r = requests.post(url, auth=(username,password))
        token = r.json().get('token')
        url = config.url_user
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=headers)
        user_json = json.loads(r.text)
        User.adduser(user_json)
        tempuser = User(user_json.get('username'))
        login_user(tempuser)
        # return 'Hi ' + current_user.username + '! <br>' + str(user_json)
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)

# 登出
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    session['user_name'] = None
    return redirect(url_for('login'))

# 我的资料
@app.route('/myprofile/')
@login_required
def myprofile():
    return render_template('myprofile.html',username=session['user_name'])


# 常用命令
@app.route('/nomaloder/', methods=['POST', 'GET'])
@login_required
def nomaloder():
   return render_template('nomaloder.html',username=session['user_name'])

#实操视频
@app.route('/demovideo/<string:le>', methods=['POST', 'GET'])
@login_required
def demovideo(le):
    randomnumber=random.uniform(0,10000)
    if request.method == 'POST':
        #开始录制
        if request.form['submit'] == 'getURL':
            # 开始获取docker中的临时链接
            dock=docker.Client(base_url='自己的服务器:端口号')
            publicport=dock.port('sqli','80')[0]['HostPort']
            url="自己的服务器:"+publicport
            return render_template('demovideo.html',username=session['user_name'],url=url,le=le,randomnumber=randomnumber)
    return render_template('demovideo.html',username=session['user_name'],le=le,randomnumber=randomnumber)

@app.route('/upload/', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']   # 获取上传的文件
        print("file",file)
        if file and allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true 
            filename = secure_filename(file.filename)   # 获取上传文件的文件名
            if request.form['submit'] == 'Upload':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
                return '{} upload successed!'.format(filename)   # 返回保存成功的信息
    # 使用 GET 方式请求页面时或是上传文件失败时返回上传文件的表单页面
      
    return render_template('upload.html',username=session['user_name'])

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)