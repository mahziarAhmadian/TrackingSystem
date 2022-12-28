from general.utils.custom_exception import CustomException


class InvalidError:

    def invalid_serializer(self, serializer_error):
        # errors = []
        # if len(serializer_error) is not None and 'non_field_errors' not in serializer_error:
        #     for error in serializer_error:
        #         errors.append(error)
        # else:
        errors = serializer_error.get('non_field_errors', None)
        if errors is None:
            errors = []
        extra_fields = {
            'errorList': errors
        }
        raise CustomException(error_summary='INVALID_DATA_RECEIVED', extra_fields=extra_fields)
