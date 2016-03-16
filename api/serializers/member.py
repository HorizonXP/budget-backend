from rest_framework.serializers import ModelSerializer, CharField, EmailField, DateField
from api import models

class MemberSerializer(ModelSerializer):
    username = CharField(source='user.username')
    first_name = CharField(source='user.first_name')
    last_name = CharField(source='user.last_name')
    birthday = DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    email = EmailField(source='user.email')

    class Meta:
        model = models.Member
        exclude = ('family', 'user')


