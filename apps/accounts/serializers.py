from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Department


class DepartmentSerializer(serializers.ModelSerializer):
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'staff_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_staff_count(self, obj):
        return obj.staff.filter(is_active=True).count()


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'employee_id', 'email', 'full_name', 'phone',
            'department', 'department_name', 'department_code',
            'role', 'photo_profile', 'is_active', 'date_joined'
        ]
        read_only_fields = ['date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'employee_id', 'email', 'full_name', 'phone',
            'department', 'role', 'photo_profile', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'department', 'role', 'photo_profile', 'is_active']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'photo_profile']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Password lama tidak sesuai.')
        return value


class AdminResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
