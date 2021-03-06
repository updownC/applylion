# Generated by Django 3.0.3 on 2020-03-20 02:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applyapp', '0002_auto_20200320_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.EmailValidator(whitelist='올바른 이메일 주소를 입력해주세요.')], verbose_name='이메일(ID)'),
        ),
    ]
