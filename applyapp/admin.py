from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm, UserQuestionForm
from .models import User, Question


class QuestionAdmin(admin.ModelAdmin):
    form = UserQuestionForm
    add_form = UserQuestionForm

    list_display = ('user', 'name',)
    list_filter = ('user', )
    fieldsets = (
        (None, {'fields': ('user', )}),
        ('Questions', {'fields': ('q1', 'q2', 'q3', 'q4', 'q5', 'q6')}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'sign_date', 'is_admin')
    list_filter = ('sign_date',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('name', 'student_id', 'department', 'department2', 'phone', 'interview_date')}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'student_id', 'password1', 'password2', 'department', 'department2', 'phone', 'interview_date')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(Group)
