from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid

# Create your models here.


class Department(models.Model):
    dept_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    dept_title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.dept_title

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Departments'


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):

        # creates a user with the parameters
        if email is None:
            raise ValueError('Email address is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            name=name.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)

    pics = models.ImageField(
        default='img/user.png', upload_to='uploads/', null=True)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True,)

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_dept = models.BooleanField(default=False)
    is_central = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'


class Reasons(models.Model):
    reason_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    reason_title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.reason_title

    class Meta:
        db_table = 'Reasons'
        verbose_name_plural = 'Reasons'


class Leave(models.Model):
    leave_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    details = models.TextField(blank=True, null=True)
    reason = models.ForeignKey(
        Reasons, on_delete=models.CASCADE, blank=True, null=True)
    dept_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} requested for a leave"

    class Meta:
        db_table = 'Leave'
        verbose_name_plural = 'Leave'
