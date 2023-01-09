# Generated by Django 3.1 on 2023-01-04 14:23

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('type', models.CharField(choices=[('EMPLOYEE', 'employee'), ('CUSTOMER', 'customer')], default='CUSTOMER', max_length=8, verbose_name='User Type')),
                ('username', models.CharField(blank=True, max_length=200, null=True, verbose_name='Username')),
                ('email', models.EmailField(blank=True, max_length=200, null=True, verbose_name='E-Mail')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.", regex='^[6-9]\\d{9}$')], verbose_name='Phone Number')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is SuperUser')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is Employee')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Is Customer')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User(s)',
            },
        ),
    ]
