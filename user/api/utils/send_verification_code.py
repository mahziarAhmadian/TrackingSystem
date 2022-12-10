from user.models import VerificationCode
import random
from django.utils import timezone
from datetime import timedelta
from user.api.utils.sms_sender import SMSSender


class VerificationSender:

    def __init__(self, name="a class for sending verification code to users") -> None:
        self.name = name
        self.sms_sender = SMSSender()

    def send(self, user, code_type, send_to='phone'):
        if code_type == 'email':
            return self.send_email_verification(user=user)
        elif code_type == 'phone':
            return self.send_phone_verification(user=user)
        elif code_type == 'entrance':
            return self.send_entrance_verification(user=user, send_to=send_to)
        elif code_type == 'resetPassword':
            return self.send_reset_password_verification(user=user, send_to=send_to)
        else:
            return {}

    def get_verification_object(self, user, code_type):
        try:
            obj = VerificationCode.objects.get(user=user, type=code_type)
        except:
            return
        return obj

    def create_verification_object(self, user, code_type, code=""):
        args = {
            'type': code_type,
            'code': code if len(code) > 0 else str(random.randint(10000, 99999)),
            'sent': True,
            'user': user,
            'expired_at': timezone.now() + timedelta(minutes=2)
        }
        obj = VerificationCode(**args)
        obj.save()
        return obj

    def send_email_verification(self, user, code_type='E', only_send=False, code=""):
        verification_obj = self.get_verification_object(user=user, code_type=code_type)
        if verification_obj is not None:
            verification_obj.code = code if only_send else str(random.randint(10000, 99999))
            verification_obj.expired_at = timezone.now() + timedelta(minutes=2)
            verification_obj.save()
        else:
            verification_obj = self.create_verification_object(user=user, code_type=code_type, code=code)
        # --------------------------------------------------------------------------------
        # send email here
        # --------------------------------------------------------------------------------
        return {"error": False, "email_verification_code": verification_obj.code}

    def send_phone_verification(self, user, code_type='P', only_send=False, code=""):
        verification_obj = self.get_verification_object(user=user, code_type=code_type)
        if verification_obj is not None:
            verification_obj.code = code if only_send else str(random.randint(10000, 99999))
            verification_obj.expired_at = timezone.now() + timedelta(minutes=2)
            verification_obj.save()
        else:
            verification_obj = self.create_verification_object(user=user, code_type=code_type, code=code)
        try:
            if code_type == 'P':
                bulk_id = self.send_verification_code(phone_number=user.phone_number,
                                                      verification_code=verification_obj.code)
            elif code_type == 'EN' or code_type == 'RST':
                bulk_id = self.send_entrance_code(phone_number=user.phone_number,
                                                  entrance_code=verification_obj.code)
        except:
            return {"error": True, "summary": "CAN_NOT_SEND_VERIFICATION_CODE",
                    "phone_verification_code": verification_obj.code}
        return {"error": False, "phone_verification_code": verification_obj.code}

    def send_entrance_verification(self, user, send_to='phone'):
        send_to = 'both'
        if send_to == 'phone':
            return {
                'phoneResult': self.send_phone_verification(user=user, code_type='EN'),
                'emailResult': None
            }
        elif send_to == 'email':
            return {
                'emailResult': self.send_email_verification(user=user, code_type='EN'),
                'phoneResult': None
            }
        elif send_to == 'both':
            code = str(random.randint(10000, 99999))
            return {
                'phoneResult': self.send_phone_verification(user=user, code_type='EN', only_send=True, code=code),
                'emailResult': self.send_email_verification(user=user, code_type='EN', only_send=True, code=code)
            }
        else:
            return {}

    def send_reset_password_verification(self, user, send_to='phone'):
        send_to = 'both'
        if send_to == 'phone':
            return {
                'phoneResult': self.send_phone_verification(user=user, code_type='RST'),
                'emailResult': None
            }
        elif send_to == 'email':
            return {
                'emailResult': self.send_email_verification(user=user, code_type='RST'),
                'phoneResult': None
            }
        elif send_to == 'both':
            code = str(random.randint(10000, 99999))
            return {
                'phoneResult': self.send_phone_verification(user=user, code_type='RST', only_send=True, code=code),
                'emailResult': self.send_email_verification(user=user, code_type='RST', only_send=True, code=code)
            }
        else:
            return {}

    def send_verification_code(self, phone_number, verification_code):
        data = {
            'phone_number': phone_number,
            'verification_code': verification_code
        }
        sms_response = self.sms_sender.send_sms(data=data, type='verification')
        return sms_response.get('bulk_id')

    def send_entrance_code(self, phone_number, entrance_code):
        data = {
            'phone_number': phone_number,
            'entrance_code': entrance_code
        }
        sms_response = self.sms_sender.send_sms(data=data, type='entrance')
        return sms_response.get('bulk_id')
