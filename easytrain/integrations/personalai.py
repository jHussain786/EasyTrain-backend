import requests
import pytz
from datetime import datetime
import time
import json

class Personalai:
    def __init__(self, key):
        self.url_data = []
        self.key = key
        self.upload_url = "https://api.personal.ai/v1/upload"
        self.validate_url = 'https://api.personal.ai/v1/api-key/validate'
        self.memory_url = 'https://api.personal.ai/v1/memory'
        self.message_url = 'https://api.personal.ai/v1/message'


    def headers(self):
        return ({
            "Content-Type": "application/json",
            "x-api-key": self.key
            })
    
    def validate_key(self):
        
        response = requests.get(self.validate_url, headers=self.headers())
        if response.status_code == 200:
            return True
        else:
            return False
    
    def memory(self, text):
        local_time = self.get_local_time()

        memory_data = {
        "Text": f"This is a test memory created at {local_time}, check your stack and see if it shows up",
        "SourceName": "Python Memory Test Script",
        "CreatedTime": local_time,
        "DeviceName": "Change this Device Name Here",
        "RawFeedText": f"<p>This is a test memory created at {local_time}, <p> with VE7LTX.CC Thanks for Testing Today!"
    }
    

        response = requests.post(self.memory_url, headers=self.headers(), json=memory_data)
        breakpoint()
        if response.status_code == 200:
            creation_status = response.json()['status']
            return creation_status
        else:
            return None
        
    def message(self, message):
        message = message + "\n"  + str(self.get_local_time)
        response = requests.post(self.message_url, headers=self.headers, json={"text": message})
        return response.json()['ai_message']

    def upload(self, urls):
        for url in urls:
            print("url: ", url)
            if url.strip() == "":
                continue
            self.url_data.append(
                {
                    "Url": url.strip(), 
                    "StartTime": self.get_local_time(),
                    "SourceApp": "EasyTrain"
                    }
                )
            
        response_ids = []
        for data in self.url_data:
            try:
                response = requests.post(self.upload_url, headers=self.headers(), data=json.dumps(data))
                response_ids.append(response.json()["status_message"]["id"])
            except Exception as e:
                self.memory(data['Url'])
                continue
        return response_ids
        
    
    def get_local_time(self):
        user_tz = datetime.now(pytz.utc).astimezone().tzinfo
        local_time = datetime.now(user_tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
        return local_time
