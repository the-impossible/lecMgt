from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid
from django.utils import timezone

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
    created = models.DateTimeField(
        verbose_name='date_created', auto_now_add=True)

    def __str__(self):
        return f"{self.user} requested for a leave"

    class Meta:
        db_table = 'Leave'
        verbose_name_plural = 'Leave'


class Notice(models.Model):
    notice_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    notice_title = models.CharField(max_length=50, unique=True)
    notice_detail = models.TextField(blank=True, null=True)
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(
        verbose_name='date_created', auto_now_add=True)

    def __str__(self):
        return f"{self.posted_by} posted a notice"

    class Meta:
        db_table = 'Notice'
        verbose_name_plural = 'Notice'


class Qualification(models.Model):
    qua_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    qua_title = models.CharField(max_length=50, unique=True)
    qua_abbr = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.qua_title}"

    class Meta:
        db_table = 'Qualification'
        verbose_name_plural = 'Qualification'


class LecturerProfile(models.Model):
    profile_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.OneToOneField(
        'User', on_delete=models.CASCADE, blank=True, null=True)
    lec_qua = models.ForeignKey(
        Qualification, on_delete=models.CASCADE, blank=True, null=True)
    position = models.ForeignKey(
        'Positions', on_delete=models.CASCADE, blank=True, null=True)
    grade_point = models.IntegerField(default=8)
    employment_date = models.DateField(
        default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id.name} profile"

    class Meta:
        db_table = 'Lecturer Profile'
        verbose_name_plural = 'Lecturer Profile'


class Positions(models.Model):
    pos_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    position_title = models.CharField(max_length=50, unique=True)
    position_grade = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.position_title}"

    class Meta:
        db_table = 'Positions'
        verbose_name_plural = 'Positions'


class Promotion(models.Model):
    pro_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    lecturer = models.ForeignKey(
        'LecturerProfile', on_delete=models.CASCADE, blank=True, null=True)
    position = models.ForeignKey(
        'Positions', on_delete=models.CASCADE, blank=True, null=True)
    dept_approval = models.BooleanField(default=False)
    central_approval = models.BooleanField(default=False)
    dean_approval = models.BooleanField(default=False)
    hod_approval = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    date_applied = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lecturer.user_id.name} is requesting for promotion"

    class Meta:
        db_table = 'Promotion'
        verbose_name_plural = 'Promotion'
