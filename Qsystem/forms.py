from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.utils import timezone


class UserForm(forms.Form):
    card_id = forms.CharField(label="身份证号", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'placeholder': "Enter Id"}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="姓名", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Username"}))
    card_id = forms.CharField(label="身份证号", max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Id"}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Password"}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    phone = forms.CharField(label="手机号", max_length=128,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': "Contact Information"}))
    #     # sex = forms.ChoiceField(label='性别', choices=gender,
    #                         widget=forms.Select(attrs={'class': 'btn btn-white dropdown-toggle'}))


class DepositForm(forms.Form):
    amount = forms.DecimalField(label="存款金额（单位：百元）", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "请输入存款金额（单位：百元）"}), max_digits=18, decimal_places=0)


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(label="取款金额（单位：百元）", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "请输入取款金额（单位：百元）"}), max_digits=18, decimal_places=0)