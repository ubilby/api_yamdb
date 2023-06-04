from rest_framework import status
from .serializers import (SignupSerializer, TokenSerializer)
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .utils import token_to_email
from rest_framework_simplejwt.tokens import AccessToken


# class для юзера
#   queryset =
#   serializer_class =
#   permission_classes =
#   pagination_class =

# для регистрации


@api_view(['POST'])
@permission_classes((AllowAny, ))
def sign_up(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    email = user.email
    token_to_email(email, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)

# для получения токена


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer._validated_data['username']
    confirmation_code = serializer._validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)
