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

@app.route('/on-click-search-bar-request', methods=['POST'])
def on_click_search_bar_request():
    j_body_data = request.get_json()
    uuid = j_body_data['search_bar_val']
    return admin.find_req_for_request(uuid)

@app.route('/on-click-search-bar-user', methods=['POST'])
def on_click_search_bar_user():
    j_body_data = request.get_json()
    val = j_body_data['search_bar_val']
    return admin.find_req_for_user(val)


@app.route('/admin-get-user-reqs', methods = ['POST'])
def admin_get_user_reqs():
    j_body_data = request.get_json()
    user_id = j_body_data['user_id']
    page = j_body_data['page']
    return admin.get_user_reqs(user_id, page['add_calc_page'], page['img_hide_page'], page['img_get_page'], page['sound_hide_page'], page['sound_get_page'])

@app.route('/admin-users-info', methods = ['POST'])
def admin_users_info():
    j_body_data = request.get_json()
    page = j_body_data['page']
    return admin.users_info(page)


@app.route('/admin-user-res-route', methods = ['POST'])
def admin_user_res_route():
    j_body_data = request.get_json()
    route = j_body_data['route']
    page = j_body_data['page']
    user_id = j_body_data['user_id']
    return admin.user_res_route(route,page,user_id)


@app.route('/admin-res-route-users', methods = ['POST'])
def admin_res_users():
    j_body_data = request.get_json()
    route = j_body_data['route']
    page = j_body_data['page']
    return admin.res_route_users(route,page)


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