from rest_framework.views import APIView
from users.models import User
from rest_framework import permissions, status
from .serializers import UserCreateSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


class SignUpView(APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer


    def signup(self,request):
        serializer = UserCreateSerializer(data=request.data):
        serializer.is_valid(raise_exception=True)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        subject = 'Регистрация на YAMDB'
        message = f'Код подтверждения: {confirmation_code}'
        send_mail(subject, message, 'YAMDB', [email])
        return Response(
            request.data,
            status=status.HTTP_200_OK
    )


    def get_token(request):
    """Получить токен для работы с API по коду подтверждения"""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)