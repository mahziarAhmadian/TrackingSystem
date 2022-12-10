from rest_framework import serializers
from user.api.utils.validation import is_email, is_phone_number, is_national_id
from user.models import User
from general.utils.custom_exception import CustomException


class ProfileSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField(source='phone_number', required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    firstName = serializers.CharField(source='first_name', required=False, allow_blank=True)
    lastName = serializers.CharField(source='last_name', required=False, allow_blank=True)
    nationalId = serializers.CharField(source='national_id', required=False, allow_blank=True)
    phoneNumberIsValid = serializers.BooleanField(source='phone_number_is_valid', read_only=True)
    emailIsValid = serializers.BooleanField(source='email_is_valid', read_only=True)
    # image = serializers.ImageField()

    class Meta:
        model = User
        fields = ('phoneNumber', 'email', 'firstName', 'lastName',
                  'nationalId', 'phoneNumberIsValid', 'emailIsValid')

    def _validate_first_name(self, first_name):
        if first_name is None:
            return {"error": False, "value": ""}
        return {"error": False, "value": first_name}

    def _validate_last_name(self, last_name):
        if last_name is None:
            return {"error": False, "value": last_name}
        return {"error": False, "value": last_name}

    def _validate_phone_number(self, phone_number):
        if phone_number is None:
            return {"error": False, "value": ''}
        if len(phone_number) == 0:
            return {"error": False, "value": ''}
        if is_phone_number(phone_number):
            return {"error": False, "value": phone_number}
        return {"error": True, "value": 'INVALID_PHONE_NUMBER'}

    def _validate_email(self, email):
        if email is None:
            return {"error": False, "value": ''}
        if len(email) == 0:
            return {"error": False, "value": ''}
        if is_email(email):
            return {"error": False, "value": email}
        return {"error": True, "value": 'INVALID_EMAIL_ADDRESS'}

    def _validate_national_id(self, national_id):
        if national_id is None:
            return {"error": False, "value": ''}
        if len(national_id) == 0:
            return {"error": False, "value": ''}
        if is_national_id(national_id):
            return {"error": False, "value": national_id}
        return {"error": True, "value": 'INVALID_NATIONAL_ID'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        # extract expected fields
        first_name = attrs.get('first_name', None)
        last_name = attrs.get('last_name', None)
        phone_number = attrs.get('phone_number', None)
        email = attrs.get('email', None)
        national_id = attrs.get('national_id', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        first_name = self._validate_first_name(first_name=first_name)
        last_name = self._validate_last_name(last_name=last_name)
        phone_number = self._validate_phone_number(phone_number=phone_number)
        email = self._validate_email(email=email)
        national_id = self._validate_national_id(national_id=national_id)
        # ----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if phone_number.get("error"):
            errors.append(phone_number.get("value"))
        if email.get("error"):
            errors.append(email.get("value"))
        if national_id.get('error'):
            errors.append(national_id.get('value'))
        # ------------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # ------------------------------------------------------------------------------------
        return {
            'phone_number': phone_number.get('value'),
            'email': email.get('value'),
            'first_name': first_name.get('value'),
            'last_name': last_name.get('value'),
            'national_id': national_id.get('value')
        }

    def phone_number_changed(self, user, phone_number):
        error_message = None
        try:
            user = User.objects.get(phone_number=phone_number, phone_number_is_valid=True)
            error_message = 'PHONE_NUMBER_EXISTS'
        except:
            user.phone_number = phone_number
            user.phone_number_is_valid = False
        if error_message is not None:
            raise CustomException(error_summary=error_message)
        return user

    def email_changed(self, user, email):
        error_message = None
        try:
            user = User.objects.get(email=email, email_is_valid=True)
            error_message = 'EMAIL_ADDRESS_EXISTS'
        except:
            user.email = email
            user.email_is_valid = False
        if error_message is not None:
            raise CustomException(error_summary=error_message)
        return user

    def update(self, user, **kwargs):
        phone_number = self.validated_data.get('phone_number', '')
        email = self.validated_data.get('email', '')
        first_name = self.validated_data.get('first_name', '')
        last_name = self.validated_data.get('last_name', '')
        national_id = self.validated_data.get('national_id', '')
        phone_changed = False
        email_changed = False
        # ----------------------------------------------------------------------------
        if len(phone_number) != 0 and phone_number != user.phone_number:
            # phone number changed, valid = False and send new verification code
            user = self.phone_number_changed(user=user, phone_number=phone_number)
            phone_changed = True
        if len(email) != 0 and email != user.email:
            # email address changed, valid = False and send new verification code
            user = self.email_changed(user=user, email=email)
            email_changed = True
        # -----------------------------------------------------------------------------
        if len(first_name) != 0:
            user.first_name = first_name
        if len(last_name) != 0:
            user.last_name = last_name
        if len(national_id) != 0:
            user.national_id = national_id
        # ----------------------------------------------------------------------------
        user.save()
        self.validated_data['phone_changed'] = phone_changed
        self.validated_data['email_changed'] = email_changed
        return user
