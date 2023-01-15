import uuid

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=Users.UserTypes.CUSTOMER)
        return queryset


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=Users.UserTypes.EMPLOYEE)
        return queryset


class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    # Utils
    class UserTypes(models.TextChoices):
        USER = "USER", "USER"
        EMPLOYEE = "EMPLOYEE", "employee"
        CUSTOMER = "CUSTOMER", "customer"

    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)

    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed."
    )

    # User Information
    type = models.CharField(
        'User Type',
        max_length=8,
        choices=UserTypes.choices,
        # Default is user is teacher
        default=UserTypes.USER
    )
    username = models.CharField('Username', max_length=200, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=200, null=True, blank=True)
    first_name = models.CharField('First Name', max_length=50, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=50, null=True, blank=True)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    phone_number = models.CharField('Phone Number', validators=[phone_regex], max_length=10, blank=True, null=True)

    # User permissions
    is_active = models.BooleanField('Is Active', default=False)
    is_admin = models.BooleanField('Is Admin', default=False)
    is_staff = models.BooleanField('Is Staff', default=False)
    is_superuser = models.BooleanField('Is SuperUser', default=False)

    # special permission which define that
    # the new user is employee or customer
    is_employee = models.BooleanField('Is Employee', default=False)
    is_customer = models.BooleanField('Is Customer', default=False)
    date_joined = models.DateTimeField('Date joined', default=timezone.now)

    USERNAME_FIELD = "username"

    # defining the manager for the UserAccount model
    objects = UserAccountManager()
    customer_objects = CustomerManager()
    employee_objects = EmployeeManager()

    class Meta:
        unique_together = ['email', 'phone_number']
        verbose_name = 'User'
        verbose_name_plural = 'User(s)'

    def __str__(self):
        if not self.username:
            return str(self.email) or str(self.phone_number)

        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

        if not self.type or self.type == None:
            self.type = Users.UserTypes.USER

        if self.email and Users.objects.filter(email=self.email).exists():
            raise ValidationError('User with this email is already registered!')

        if self.phone_number and Users.objects.filter(phone_number=self.phone_number).exists():
            raise ValidationError('User with this number is already registered!')

        return super().save(*args, **kwargs)


@receiver(pre_save, sender=Users)
def set_username(sender, instance, **kwargs):
        if not instance.username and (instance.email or instance.phone_number):
            if instance.email:
                instance.username = BaseUserManager.normalize_email(instance.email)
            else:
                instance.username = instance.phone_number


class EmailOtp(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    email = models.EmailField(blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Email Otp'
        verbose_name_plural = 'Email Otp(s)'

    def __str__(self):
        return self.email
