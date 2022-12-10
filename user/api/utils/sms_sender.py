import requests


class SMSSender:

    def __init__(self, name="a class for calling SMS API and send sms to users"):
        self.name = name
        self.sms_api = "https://sms.softomega.ir/sms-service/api/send/sms"

    def send(self, data):
        response = requests.post(url=self.sms_api, json=data)
        print(response.text)
        json_data = response.json()
        print(json_data)
        return json_data

    def send_sms(self, data, type='verification'):
        if type == 'verification':
            phone_number = data.get('phone_number')
            verification_code = data.get('verification_code')
            sms_data = {
                "username": "OMEGA_test",
                "password": "OMEGA1398!",
                "destination": str(phone_number),
                "pattern_values": {
                    "verification-code": str(verification_code)
                }
            }
        elif type == 'entrance' or type == 'reset_password':
            phone_number = data.get('phone_number')
            entrance_code = data.get('entrance_code')
            sms_data = {
                "username": "badro_post",
                "password": "CPYgGq7Z",
                "destination": str(phone_number),
                "pattern_values": {
                    "entrance-code": str(entrance_code)
                }
            }
        else:
            return
        return self.send(data=sms_data)
