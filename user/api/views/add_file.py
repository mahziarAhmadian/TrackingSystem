from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserImageSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import User
from user.api.utils import check_field, invalid_error


class UserImage(APIView):
    serializer_class = UserImageSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        required_fields = ['SmImage', 'MdImage', 'LgImage']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data)
        if not serializer.is_valid():
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='FILE_ADDED')
        return Response(data=data, status=data.get('statusCode'))
