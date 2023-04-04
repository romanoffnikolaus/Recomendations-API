from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **kwargs):
        if not email:
            raise ValueError(
                'Введите email'
            )
        if not password:
            raise ValueError(
                'Введите пароль'
            )
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(
                'Введите email'
            )
        if not password:
            raise ValueError(
                'Введите пароль'
            )
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    choices = (('m', 'Male'),('f','Female'))
    sex = models.CharField(choices=choices, max_length=1, blank=True, help_text='Укажите пол')
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)    
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return f'{self.id} -> {self.email} -- {self.first_name}'

    def create_activation_code(self):
        code = get_random_string(
            length=10,
            allowed_chars='1234567890#?$%&'
        )
        self.activation_code = code
        self.save()
