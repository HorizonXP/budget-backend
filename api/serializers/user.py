from rest_framework.serializers import ModelSerializer, CharField, DateField, ValidationError, SerializerMethodField
from django.contrib.auth import get_user_model
from .member import MemberSerializer

class UserSerializer(ModelSerializer):
    current_password = CharField(
        write_only=True,
        required=False,
        allow_null=True,
        label="Current Password",
        help_text="Enter your current password.",
        style={'input_type': 'password'}
    )
    new_password1 = CharField(
        write_only=True,
        required=False,
        allow_null=True,
        label="New Password",
        help_text="Enter your new password.",
        style={'input_type': 'password'}
    )
    new_password2 = CharField(
        write_only=True,
        required=False,
        allow_null=True,
        label="Retype New Password",
        help_text="Re-enter your new password.",
        style={'input_type': 'password'}
    )
    family = SerializerMethodField()
    birthday = DateField(source='member.birthday', required=False, format='%d/%m/%Y', input_formats=['%d/%m/%Y'])

    def get_family(self, obj):
        from .family import FamilySerializer
        if (obj.member):
            return FamilySerializer(obj.member.family).data
        else:
            return None

    def validate(self, data):
        current_password = data['current_password'] if 'current_password' in data else None
        new_password1 = data['new_password1'] if 'new_password1' in data else None
        new_password2 = data['new_password2'] if 'new_password2' in data else None

        if current_password is not None:
            if new_password1 is None or len(new_password1) < 6:
                raise ValidationError({
                    'new_password1': "Your new password must be longer than 6 characters."
                })
            elif new_password1 == current_password:
                raise ValidationError({
                    'new_password1': "Your new password has to be different from your existing password."
                })
            elif new_password1 != new_password2:
                raise ValidationError({
                    'new_password2': "Your new password entries do not match."
                })
        else:
            if new_password1 is not None or new_password2 is not None:
                raise ValidationError({
                    'current_password': "You must enter your current password before you can change it."
                })
        return data

    def update(self, instance, validated_data):
        current_password = validated_data['current_password'] if 'current_password' in validated_data else None
        new_password1 = validated_data['new_password1'] if 'new_password1' in validated_data else None
        new_password2 = validated_data['new_password2'] if 'new_password2' in validated_data else None
        member = validated_data['member'] if 'member' in validated_data else None
        birthday = None
        if member:
            birthday = member['birthday'] if 'birthday' in member else None
            del validated_data['member']
        if current_password is not None:
            if instance.check_password(current_password):
                instance.set_password(new_password1)
            else:
                # Wrong password
                raise ValidationError({
                    'current_password': "You entered the wrong password."
                })
        if birthday:
            instance.member.birthday = birthday
            instance.member.save()
        return super(UserSerializer, self).update(instance, validated_data)


    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'birthday', 'family', 'current_password', 'new_password1', 'new_password2')

