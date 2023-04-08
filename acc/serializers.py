from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    username_field = 'email'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email__iexact=attrs.get("email")).first() or None
        if user_obj is not None:
            credentials = {
                'email': user_obj.email,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)
                    payload = self.jwt_payload_handler(user)
                    return {
                        'token': self.jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)
        else:
            msg = _('Account with this email address does not exist.')
            raise serializers.ValidationError(msg)