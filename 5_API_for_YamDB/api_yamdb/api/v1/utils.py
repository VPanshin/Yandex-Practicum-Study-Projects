from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def generating_and_sending_confirmation_code(user):
    """
    Генерируем confirmation_code и отправляем пользователю email,
    содержащий данный confirmation_code.
    """
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Ваш код для подтверждения регистрации',
        (f'Добрый день, {user.username}!\n'
         f'Ваш код подтверждения регистрации: {confirmation_code}'),
        settings.ADMIN_EMAIL,
        [user.email],
        fail_silently=False
    )
