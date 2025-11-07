from rest_framework import serializers
from .models import User, Company, UserCompanyRole, UserSettings


class CompanySerializer(serializers.ModelSerializer):
    AdminUserID = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Company
        fields = ('CompanyID', 'CompanyName', 'CompanyNotes', 'AdminUserID', 'CreatedDate')
        read_only_fields = ('CompanyID', 'CreatedDate')


class UserSerializer(serializers.ModelSerializer):
    ProfilePhoto = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',  # Auth ID remains lower-case from Django core
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'is_staff',
            'is_superuser',
            'ProfilePhoto',
        )
        read_only_fields = ('id', 'date_joined', 'is_staff', 'is_superuser')

    def get_ProfilePhoto(self, obj):
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and 'profile_photo' in request.FILES:
            instance.profile_photo = request.FILES['profile_photo']

        for attr, value in validated_data.items():
            if attr != 'profile_photo':
                setattr(instance, attr, value)

        instance.save()
        return instance


class UserCompanyRoleSerializer(serializers.ModelSerializer):
    Company = CompanySerializer(source='CompanyID', read_only=True)

    class Meta:
        model = UserCompanyRole
        fields = (
            'UserCompanyRoleID',
            'UserID',
            'CompanyID',
            'Role',
            'CreatedDate',
            'Company',
        )
        read_only_fields = ('UserCompanyRoleID', 'CreatedDate', 'UserID')


class UserSettingsSerializer(serializers.ModelSerializer):
    DefaultCompany = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        allow_null=True,
        required=False,
    )
    DefaultCompanyDetails = CompanySerializer(source='DefaultCompany', read_only=True)

    class Meta:
        model = UserSettings
        fields = (
            'UserID',
            'EmailNotifications',
            'DesktopNotifications',
            'NotificationTypes',
            'AutoSaveForms',
            'DefaultCompany',
            'DefaultCompanyDetails',
            'DateFormat',
            'CurrencyFormat',
            'Theme',
            'TwoFactorEnabled',
            'SessionTimeout',
            'LastExportDate',
            'CreatedDate',
            'ModifiedDate',
        )
        read_only_fields = ('UserID', 'LastExportDate', 'CreatedDate', 'ModifiedDate')
