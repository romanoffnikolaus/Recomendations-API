from core.celery import app
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


@app.task
def send_activation_code_celery(email, activation_code):
    context = {
        'text_detail': 'спасибо за регистрацию',
        'email': email,
        'domain': 'http://127.0.0.1:8000',
        'activation_code': activation_code
    }
    msg_html = render_to_string('activation.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Активация аккаунта!',
        message,
        'recomendations@gmail.com',
        [email],
        html_message=msg_html,
        fail_silently=False
    )


@app.task
def send_recovery_code_celery(email, activation_code):
    context = {
        'text_detail': 'Доброго дня. Ваша ссылка для сброса пароля.',
        'email': email,
        'domain': 'http://127.0.0.1:8000',
        'activation_code': activation_code,
        'action': 'Пройдите по ссылке для продолжения восстановления',
        'path': '/api/v1/forgot_password_complete/'
    }
    msg_html = render_to_string('recovery.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Восстановление пароля',
        message,
        'recomendations@gmail.com',
        [email],
        html_message=msg_html,
        fail_silently=False
    )