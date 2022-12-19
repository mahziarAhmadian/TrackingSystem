from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserImageSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import UserImage
from user.api.utils import check_field, invalid_error
import os


class UserImageView(APIView):
    serializer_class = UserImageSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, image_id):

        try:
            image_object = UserImage.objects.get(id=image_id)
        except:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='IMAGE_NOT_EXISTS', extra_fields=extra_fields)
        return image_object

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        required_fields = ['SmImage', 'MdImage', 'LgImage']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        input_data['user'] = user.id
        serializer = self.serializer_class(data=input_data)
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='FILE_ADDED')
        return Response(data=data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        image_id = self.check_field.check_field(input_data=input_data, required_field='imageId')
        image_object = self.get_object(image_id=image_id)
        check_field = {
            "sm_image": image_object.sm_image,
            "md_image": image_object.md_image,
            "lg_image": image_object.lg_image,
        }
        base_dir = os.getcwd()
        media_dir = os.path.join(base_dir, 'media')
        try:
            for field in check_field:
                if bool(check_field[field]):
                    media_file_path = os.path.join(media_dir, str(check_field[field]))
                    if os.path.exists(media_file_path):
                        os.remove(media_file_path)
        except:
            pass
        image_object.delete()
        data = generate_response(keyword='FILE_DELETED')
        return Response(data=data, status=data.get('statusCode'))
