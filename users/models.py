from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, name, email, password=None):
        if not username:
            raise ValueError('Users must have an ID')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            name=name,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, email, password=None):
        user = self.create_user(
            username=username,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True, primary_key=True) 
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_image = models.ImageField(blank=True, null=True)
    attendance_score = models.IntegerField(default=0)
    participation_score = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friend_set', blank=True)  # 친구 목록

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username
