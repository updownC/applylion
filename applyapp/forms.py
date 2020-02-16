from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User, Question


class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('q1', 'q2', 'q3', 'q4', 'q5', 'q6')
        widgets = {'q1': forms.Textarea(attrs={'class': 'form-control2'}),
                   'q2': forms.Textarea(attrs={'class': 'form-control2'}),
                   'q3': forms.Textarea(attrs={'class': 'form-control2'}),
                   'q4': forms.Textarea(attrs={'class': 'form-control2'}),
                   'q5': forms.Textarea(attrs={'class': 'form-control2'}),
                   'q6': forms.Textarea(attrs={'class': 'form-control3', 'placeholder': '예) 20-1학기 경영전략학회 *****에서 활동할 예정입니다. '}),
                   }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email(ID)'}),
        }


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호를 한번 더 입력해주세요.'}))
    agree = forms.BooleanField(label='동의')

    CHOICES = [('토', '21(토)'), ('일', '22(일)'), ('양일', '모두 가능')]
    interview_date = forms.CharField(
        label='면접가능 날짜', widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = User
        fields = ('email', 'student_id', 'department',
                  'department2', 'name', 'phone', 'interview_date')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '경영학과'}),
            'department2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '생략 가능합니다.'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '010-1234-5678'}),
            'interview_date': forms.CharField(label='면접가능 날짜', widget=forms.RadioSelect(choices=[('토', '21(토)'), ('일', '22(일)'), ('양일', '모두 가능')]))
        }

    field_order = ['email', 'password1', 'password2', 'name', 'student_id',
                   'department', 'department2', 'phone', 'interview_date', 'agree']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 맞지 않습니다.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('이미 사용중인 이메일 입니다.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'student_id', 'department',
                  'department2', 'phone', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
