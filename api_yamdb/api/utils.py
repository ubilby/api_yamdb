from django.core.mail import send_mail


def token_to_email(email, confirmation_code):
    send_mail(
        'Код подтверждения для api yamdb',
        f' Ваш код подтверждения: {confirmation_code}',
        [f'{email}'],
        fail_silently=False,
    )
