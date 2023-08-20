import requests
import json
from App import config
from App.Controller import db_postgres_controller as db

username = config.configs['API_USERNAME']
password = config.configs['API_PASSWORD']


class Api:
        
    def __init__(self):
        self.target_api_url = config.configs["TARGET_API_URL"]
        self.dom_address = config.configs['DOMAIN_ADDRESS']
        self.headers = { 'Content-Type': 'application/json','Authorization': ''}

    def get_new_access_token(self):
        url = self.target_api_url + '/signin'
        payload = json.dumps({
            "username": username,
            "password": password
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.headers['Authorization'] = json.loads(response.text)['result']['token']
        
    
    def check_expired_token(self,response, url, payload):
        response = json.loads(response)
        if response['result'] == 'ExpiredToken':
            self.get_new_access_token()
            response = requests.request("POST", url, headers=self.headers, data=payload)
            return response
        else:
            return 'notExpired'
        
        
    # Get the results of the requests that were in the queue
    def get_res_from_api(self,api_req_id):
        target_api_url = self.target_api_url + '/get-result'
        payload = json.dumps({
            "request_id": api_req_id
            })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()   
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
        
        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)
    

    def add_two_numbers(self,num1,num2):
        target_api_url = self.target_api_url + '/add-two-numbers'
        payload = json.dumps({
        "params": {
            "num1": num1,
            "num2": num2
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)

        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)

    

    def hide_text_in_image(self, text, url):
        target_api_url = self.target_api_url + '/hide-text-in-image'
        payload = json.dumps({
        "params": {
            "url": url,
            "text": text
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
      
        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)

      
    def get_hidden_text_from_image(self, url):
        target_api_url = self.target_api_url + '/get-hidden-text-from-image'
        payload = json.dumps({
        "params": {
            "url": url
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)

        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)

      
    def hide_text_in_sound(self, text, url):
        target_api_url = self.target_api_url + '/hide-text-in-sound'
        payload = json.dumps({
        "params": {
            "url": url,
            "text": text
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
    
        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)


    def get_hidden_text_from_sound(self, url):
        target_api_url = self.target_api_url + '/get-hidden-text-from-sound'
        payload = json.dumps({
        "params": {
            "url": url
            }
        })
        if self.headers['Authorization'] == '':
            self.get_new_access_token()
        response = requests.request("POST", target_api_url, headers=self.headers, data=payload)
    
        # Check is expired token. if is then get new access token and send new request
        res = self.check_expired_token(response.text, target_api_url, payload)
        if res == 'notExpired' :
            return json.loads(response.text)
        return json.loads(res.text)

    

api = Api()






