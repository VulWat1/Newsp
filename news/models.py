from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Users(BaseUserManager): 
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_editor', False)
        extra_fields.setdefault('is_publicer', False)
        return self._create_user(email, password, **extra_fields)    
    
    def create_editor(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_publicer', False)
        return self._create_user(email, password, **extra_fields)    
    
    def create_publicer(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_editor', False)
        extra_fields.setdefault('is_publicer', True)
        return self._create_user(email, password, **extra_fields)    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_publicer', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=False)

    is_publicer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = Users()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __full__(self):
        return self.name
    def __short__(self):
        return self.name or self.email.split('@')[0]

class Articles(models.Model):
    author = models.CharField('Автор', max_length=50, default=f"Kudaibergen")
    title = models.CharField('Заголовок новости', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата и время публикации')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
