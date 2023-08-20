from App.Controller import db_postgres_controller as db
from App.Controller.api_controller import api
import json
import os
from App import config
import requests
import uuid

def process(req_uuid):
    db.db.updateInRequest(req_uuid, 0 ,'processing')
    
    # Get route and params
    req_info = db.db.getReqInfo(req_uuid)
    
    route = req_info[0][2]
    if route == '/add-two-numbers':
        result = add(req_info[0])
    elif route == '/hide-text-in-image':
        result = hide_text(req_info[0])
    elif route == '/get-hidden-text-from-image':        
        result = get_text(req_info[0])
    elif route == '/hide-text-in-sound':
        result = hide_in_sound(req_info[0])
    elif route == '/get-hidden-text-from-sound':
        result = get_from_sound(req_info[0])
    else:
        return
    
    print('\nresult:::::::;: ',result)
    db.db.updateInRequest(req_uuid, result['request_id'], result['result'])
    return 'true'
    

def add(info):
    res = api.add_two_numbers(int(info[3]["num1"]) , int(info[3]["num2"]))
    return res


def hide_in_sound(info):     
    text = info[3]["text"]
    
    # save image before hide process in local storage
    audio_url_before_hide = save_media(result=info[3], route=info[2], user_id=info[1])
    params = json.dumps({'url':audio_url_before_hide['result']['url'], 'text':text})
    db.db.changeParams(params=params, uuid=info[8])
    
    audio_path = info[3]["url"]
    res = api.hide_text_in_sound(text, audio_path) # Send audio url to core api
    return res

def get_from_sound(info): 
    # save audio before extract process in local storage
    audio_url_before_hide = save_media(result=info[3], route=info[2], user_id=info[1])
    params = json.dumps(audio_url_before_hide['result'])
    db.db.changeParams(params=params, uuid=info[8])
    
    url = info[3]["url"]
    res = api.get_hidden_text_from_sound(url)
    return res
    
def hide_text(info):
    text = info[3]["text"]
    
    # save image before hide process in local storage
    img_url_before_hide = save_media(result=info[3], route=info[2], user_id=info[1])
    params = json.dumps({'url':img_url_before_hide['result']['url'], 'text':text})
    db.db.changeParams(params=params, uuid=info[8])
    
    image_path = info[3]["url"]
    res = api.hide_text_in_image(text, image_path) # Send image url to core api
    return res

def get_text(info):
    # save image before extract process in local storage
    img_url_before_hide = save_media(result=info[3], route=info[2], user_id=info[1])
    params = json.dumps(img_url_before_hide['result'])
    db.db.changeParams(params=params, uuid=info[8])
    
    image_path = info[3]["url"]
    res = api.get_hidden_text_from_image(image_path)
    return res


# Save media in local storage
def save_media(result,route, user_id):
    config_path = '.' + config.configs["UPLOAD_USER_FILE"] + str(user_id) + '/'
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        
    if route == '/hide-text-in-image' or route == '/get-hidden-text-from-image':
        format = '.png'
    elif route == '/hide-text-in-sound' or route == '/get-hidden-text-from-sound':
        format = '.wav'
    
    response = requests.get(result['url'])
    path = config_path + uuid.uuid4().hex + format
    with open(path, 'wb') as file:
        file.write(response.content)
        
    result = {'result':{'url':path}}
    return result


def result(req_uuid,user_id):
    # Get request process result if there is in process table
    res = db.db.getReqRes(req_uuid, user_id)
    if res == []:
        # There is no the request in request table
        res = {"result":"request id is wrong" , "status-code":400}
        return res
        
    elif res[0][0] is None or res[0][1] != 'done' :
        result = api.get_res_from_api(res[0][3])
        if result['status-code'] == 200:
            media_route = ['/hide-text-in-image', '/hide-text-in-sound']
            if res[0][2] in media_route:    
                 # The media path(url) is from core api. i save it in local storage and change path to local
                result = save_media(result['result'], res[0][2], user_id) 
                
            db.db.updateResFromApi(status='done', result= json.dumps({'result': result['result']}), req_uuid=req_uuid)
            res = {"result":result["result"] , "request_id":req_uuid , "status-code":200 , "type":res[0][2] }    
        else:        
            # request accepted but not processed yet 
            res = {"result":"processing" , "request_id":req_uuid , "status-code":202}
        return res

    # Process is done
    res = {"result":res[0][0]["result"] , "request_id":req_uuid , "status-code":200 , "type":res[0][2] }
    
    return res