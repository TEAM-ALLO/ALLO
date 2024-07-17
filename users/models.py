from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, id, name, email, password=None):
        if not id:
            raise ValueError('Users must have an ID')
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            id=id,
            name=name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, name, email, password=None):
        user = self.create_user(
            id=id,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.CharField(max_length=15, unique=True, primary_key=True) 
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.id
    
