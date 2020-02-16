from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils import timezone
from django.core.validators import EmailValidator
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('이메일은 필수 입력사항입니다.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    CHOICES = [('토', '21(토)'), ('일', '22(일)'), ('양일', '모두 가능')]
    email = models.EmailField(
        verbose_name='이메일(ID)',
        max_length=255,
        unique=True,
        validators=[EmailValidator(whitelist="올바른 이메일 주소를 입력해주세요.")]
    )
    student_id = models.CharField(verbose_name='학번', max_length=100, null=True)
    department = models.CharField(
        verbose_name='전공', max_length=150, null=True)
    department2 = models.CharField(
        verbose_name='이중/융합전공', max_length=150, null=True, blank=True)
    name = models.CharField(verbose_name='이름', max_length=50, null=True)
    phone = models.CharField(verbose_name='연락처', max_length=100, null=True)
    interview_date = models.CharField(
        max_length=10, verbose_name='인터뷰 가능일', choices=CHOICES, null=True)
    sign_date = models.DateTimeField(verbose_name='생성일', default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Question(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    q1 = models.TextField(verbose_name='지원동기 (1000자 내외)', max_length=2000)
    q2 = models.TextField(
        verbose_name='향후 5년 계획과, 10년 후의 나의 모습을 이야기해 주세요. (1000자 내외)', max_length=2000)
    q3 = models.TextField(
        verbose_name='인생에서 가장 도전적이었던 경험과, 그 경험을 통해 얻은 것과 잃은 것은 무엇인가요? (1000자 내외)', max_length=2000)
    q4 = models.TextField(
        verbose_name='만들고 싶은 서비스와 그 계기 및 이유를 설명해 주세요. (1000자 내외)', max_length=2000)
    q5 = models.TextField(
        verbose_name='멋사 활동을 통해 얻고 싶은 것과 자신이 멋사에 기여할 수 있는 것은 무엇인지 이야기해 주세요. (1000자 내외)', max_length=2000)
    q6 = models.TextField(
        verbose_name='멋사외에 활동했던, 혹은 활동 예정인 동아리나 학회가 있으면 간략하게 적어주세요.(없으면 생략가능)', max_length=400, null=True, blank=True)
    created_date = models.DateTimeField(
        verbose_name='등록일', default=timezone.now)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
