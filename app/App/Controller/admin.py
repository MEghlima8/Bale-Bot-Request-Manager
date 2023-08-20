import json
from App.Controller import db_postgres_controller as db
import math

def find_req_for_request(uuid):
    res = db.db.getReqInfo(uuid)
    return res

def find_req_for_user(val):
    res = db.db.getUserInfo(val)
    return res


def get_dashboard_info():
    users_reqs_status = db.db.admin_getUsersRequestsStatus()
    dict_result = {"status-code":200, "result": {"done":0 , "in queue":0 , "processing":0}}
    for i in users_reqs_status:
        dict_result["result"][i[0]] = i[1]
    
    dict_result["result"]["all_add_reqs"] = db.db.admin_getAllReq('/add-two-numbers', None)[0][0]
    dict_result["result"]["all_img_steg_reqs"] = db.db.admin_getAllReq('/hide-text-in-image', '/get-hidden-text-from-image')[0][0]
    dict_result["result"]["all_audio_steg_reqs"] = db.db.admin_getAllReq('/hide-text-in-sound', '/get-hidden-text-from-sound')[0][0]

    j_result = json.dumps(dict_result) 
    return j_result


def res_steg_img():
    users_steg_img_req_status = db.db.admin_route_reqs_status('/hide-text-in-image')
    result = {"status-code":200 , "result":users_steg_img_req_status}
    j_result = json.dumps(result)
    return j_result

def res_extr_steg_img():
    users_extr_steg_img_req_status = db.db.admin_route_reqs_status('/get-hidden-text-from-image')
    result = {"status-code":200 , "result":users_extr_steg_img_req_status}
    j_result = json.dumps(result)
    return j_result
 
def res_steg_audio():
    users_steg_audio_req_status = db.db.admin_route_reqs_status('/hide-text-in-sound')
    result = {"status-code":200 , "result":users_steg_audio_req_status}
    j_result = json.dumps(result)
    return j_result

def res_extr_audio():
    users_extr_steg_audio_req_status = db.db.admin_route_reqs_status('/get-hidden-text-from-sound')
    result = {"status-code":200 , "result":users_extr_steg_audio_req_status}
    j_result = json.dumps(result)
    return j_result


def get_items_from_offset(page,all_items):
    offset = (page - 1) * 10  # There are 10 requests per page
    items = all_items[offset: offset+10]
    count_all_pages = math.ceil(len(all_items) / 10) # Get count of all pages: if all_req = 25 then return 3
    return items,count_all_pages

# Get route results for all users
def res_route_users(route,page):
    res_users_reqs = db.db.admin_route_reqs_status(route)
    page_items,count_all_pages = get_items_from_offset(page,res_users_reqs)
    result = {"status-code":200 , "result":page_items, 'count_pages':count_all_pages, 'active_page':page}
    j_result = json.dumps(result)
    return j_result 
 
# Get route results for a user
def user_res_route(route,page,user_id):
    res_user_reqs = db.db.admin_user_route_reqs_status(route,user_id)
    page_items,count_all_pages = get_items_from_offset(page,res_user_reqs)
    result = {"status-code":200 , "result":page_items, 'count_pages':count_all_pages, 'active_page':page}
    j_result = json.dumps(result)
    return j_result
 
# Return all user requests
def get_user_reqs(user_id,add_calc_page, img_hide_page, img_get_page, sound_hide_page, sound_get_page):
    add_calc = db.db.admin_userRes('/add-two-numbers',user_id)
    add_calc_items, count_pages_add_calc = get_items_from_offset(add_calc_page,add_calc)
    
    img_hide = db.db.admin_userRes('/hide-text-in-image',user_id)
    img_hide_items, count_pages_img_hide = get_items_from_offset(img_hide_page,img_hide)
    
    img_get = db.db.admin_userRes('/get-hidden-text-from-image',user_id)
    img_get_items, count_pages_img_get = get_items_from_offset(img_get_page,img_get)
    
    sound_hide = db.db.admin_userRes('/hide-text-in-sound',user_id)
    sound_hide_items, count_pages_sound_hide = get_items_from_offset(sound_hide_page,sound_hide)
    
    sound_get = db.db.admin_userRes('/get-hidden-text-from-sound',user_id)
    sound_get_items, count_pages_sound_get = get_items_from_offset(sound_get_page,sound_get)
        
    result = {"status-code" : 200 ,
              "result" : {"add_calc": [add_calc_items,count_pages_add_calc],
                          "img_hide": [img_hide_items,count_pages_img_hide],
                          "img_get": [img_get_items, count_pages_img_get],
                          "sound_hide": [sound_hide_items, count_pages_sound_hide],
                          "sound_get": [sound_get_items, count_pages_sound_get]
                          }
              }
    j_result = json.dumps(result)
    return j_result
   

# users info
def users_info(page):
    res_users_info = db.db.admin_get_users_info()    
    page_items, count_all_pages = get_items_from_offset(page,res_users_info)
    result = {"status-code":200 , "result":page_items, 'count_pages':count_all_pages, 'active_page':page}
    j_result = json.dumps(result)
    return j_result