from rest_framework import serializers
from user.models import User, UserProfile
from user.api.utils.validation import is_phone_number, is_type


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})
        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True,
        kwargs['required'] = False  # required True checked on validation code by my self
        super().__init__(*args, **kwargs)


class RegisterSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    # required True checked on validation code by my self
    phoneNumber = serializers.CharField(source='phone_number', required=False)
    password = PasswordField()
    userType = serializers.CharField(source='type', required=False,allow_null=True,allow_blank=True)

    class Meta:
        model = User
        fields = ('phoneNumber', 'password', 'userType', 'firstName', 'lastName')

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
            return {"error": True, "value": 'PHONE_NUMBER_REQUIRED'}
        if is_phone_number(phone_number):
            return {"error": False, "value": phone_number}
        return {"error": True, "value": 'INVALID_PHONE_NUMBER'}

    def _validate_password(self, password):
        if password is None:
            return {"error": True, "value": 'PASSWORD_REQUIRED'}
        if len(password) < 6:
            return {"error": True, "value": 'SHORT_LENGTH_PASSWORD'}
        return {"error": False, "value": password}

    def _validate_type(self, user_type):
        if user_type is None:
            return {"error": False, "value": None}
        is_type_response = is_type(user_type)
        print(f"is type response is : {is_type_response}")
        if is_type_response:
            return {"error": False, "value": is_type_response[1]}
        return {"error": True, "value": 'INVALID_USER_TYPE'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        # extract expected fields
        first_name = attrs.get('first_name', None)
        last_name = attrs.get('last_name', None)

        phone_number = attrs.get('phone_number', None)
        password = attrs.get('password', None)
        user_type = attrs.get('type', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        first_name = self._validate_first_name(first_name=first_name)
        last_name = self._validate_last_name(last_name=last_name)
        phone_number = self._validate_phone_number(phone_number=phone_number)
        password = self._validate_password(password=password)
        user_type = self._validate_type(user_type=user_type)
        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if phone_number.get("error"):
            errors.append(phone_number.get("value"))
        if password.get("error"):
            errors.append(password.get("value"))
        if user_type.get("error"):
            errors.append(user_type.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
            'first_name': first_name.get('value'),
            'last_name': last_name.get('value'),
            'phone_number': phone_number.get('value'),
            'password': password.get('value'),
            'user_type': user_type.get('value')
        }
        # ---------------------------------------------------------------------------------
        return validated_data

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = User.objects.create_user(phone_number=phone_number,
                                        password=password,
                                        type=user_type,
                                        **validated_data)
        profile = UserProfile(first_name=first_name, last_name=last_name)
        profile.save()
        user.profile = profile
        user.save()

        return user
