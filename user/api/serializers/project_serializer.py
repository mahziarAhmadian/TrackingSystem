from rest_framework import serializers
from user.models import Project, User
from user.api.serializers.user_serializer import UserSerializer
from general.utils.custom_exception import CustomException


class ProjectSerializer(serializers.ModelSerializer):
    englishName = serializers.CharField(source='english_name', required=True, allow_blank=True)
    persianName = serializers.CharField(source='persian_name', required=True, allow_blank=True)
    image = serializers.ImageField(allow_null=True, use_url=True)
    location = serializers.CharField(max_length=255, allow_blank=True)
    locationRange = serializers.JSONField(source='location_range', allow_null=True)
    startedFrom = serializers.DateTimeField(source='started_from')
    deadline = serializers.DateTimeField()
    contractNumber = serializers.CharField(source='contract_number', max_length=255, allow_blank=True)
    contractInformation = serializers.JSONField(source='contract_information', allow_null=True)
    information = serializers.JSONField()
    employerInfo = serializers.SerializerMethodField()
    ownerInfo = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'englishName', 'image', 'persianName', 'location', 'locationRange', 'startedFrom', 'deadline',
                  'contractNumber', 'contractInformation', 'information', 'employerInfo', 'ownerInfo')

    def get_employerInfo(self, project):
        user = User.objects.get(id=project.employer.id)
        result = UserSerializer(user).data
        pop_field = ['Id', 'PhoneNumberIsValid', 'isStaff', 'isActive', 'isSuperuser', 'Notes', 'permissions',
                     'Blocked', 'profile', 'Images']
        for field in pop_field:
            result.pop(field)
        return result

    def get_ownerInfo(self, project):
        if project.owner is None:
            return None
        user = User.objects.get(id=project.owner.id)
        result = UserSerializer(user).data
        pop_field = ['Id', 'PhoneNumberIsValid', 'isStaff', 'isActive', 'isSuperuser', 'Notes', 'permissions',
                     'Blocked', 'profile', 'Images']
        for field in pop_field:
            result.pop(field)
        return result


    # def to_representation(self, instance):
    #     request = self.context
    #     rep = super().to_representation(instance)
    #     req = request.get('request')
    #     return rep
