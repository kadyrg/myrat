from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('type', User.UserType.MANAGER)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save_super(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        EMPLOYEE = 'employee', 'Employee'

    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=UserType, default=UserType.EMPLOYEE)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    new_password = models.CharField(max_length=50, null=True, blank=True)
    hourly_salary = models.DecimalField(max_digits=15, decimal_places=2)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
        
    def save(self, *args, **kwargs):
        if self.type == self.UserType.MANAGER:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
            super().save(*args, **kwargs)

        if self.new_password:
            self.set_password(self.new_password)
            self.new_password = None
        super().save(*args, **kwargs)

    def save_super(self, *args, **kwargs):
        super().save(*args, **kwargs)
