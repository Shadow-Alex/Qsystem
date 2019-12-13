from captcha.fields import CaptchaField
from django import forms
from django.utils import timezone


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


class QuestionForm(forms.Form):
    options = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    question_text = forms.CharField(
        label="题干",
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correctOption = forms.ChoiceField(
        label='正确选项(只支持单选题)',
        choices=options,
        widget=forms.Select(attrs={'class': 'form-control'})  # Just for testing. 可以删除attrs。
    )
    A_text = forms.CharField(
        label="A:",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    B_text = forms.CharField(
        label="B:",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    C_text = forms.CharField(
        label="C:",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    D_text = forms.CharField(
        label="D:",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class PaperHeadForm(forms.Form):
    paperTitle = forms.CharField(
        label='卷名',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
