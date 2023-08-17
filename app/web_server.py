from App import config
from flask import Flask, request, render_template, session
from App.Controller import admin

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/on-click-search-bar', methods=['POST'])
def on_click_search_bar():
    j_body_data = request.get_json()
    uuid = j_body_data['search_bar_val']
    return admin.find_req_with_uuid(uuid)


@app.route('/admin-get-user-reqs', methods = ['POST'])
def admin_get_user_reqs():
    j_body_data = request.get_json()
    user_id = j_body_data['user_id']
    return admin.get_uesr_reqs(user_id)

@app.route('/admin-res-add-calc', methods = ['POST'])
def admin_res_add_calc():
    return admin.res_add_calc()

@app.route('/admin-res-steg-img', methods = ['POST'])
def admin_res_steg_img():
    return admin.res_steg_img()

@app.route('/admin-res-extr-steg-img', methods = ['POST'])
def admin_res_extr_steg_img():
    return admin.res_extr_steg_img()

@app.route('/admin-res-steg-audio', methods = ['POST'])
def admin_res_steg_audio():
    return admin.res_steg_audio()

@app.route('/admin-res-extr-audio', methods = ['POST'])
def admin_res_extr_audio():
    return admin.res_extr_audio()

@app.route('/admin-users-info', methods = ['POST'])
def admin_users_info():
    return admin.users_info()


# Signin admin
@app.route('/signin' ,methods=['POST'])
def signin():
    j_body_data = request.get_json()
    s_username = j_body_data['username']
    s_password = j_body_data['password']
    if s_username == 'admin' and s_password == 'admin':
        session['admin'] = True
        return admin.get_dashboard_info()


def main():
    app.run(host=config.configs['HOST'], port=config.configs['PORT'])