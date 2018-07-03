from django import forms
from django.contrib.auth.models import User
from django.contrib import auth

from .models import UserInfo, UserProfile


class LoginForm(forms.Form):  # 创建登录表单
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):  # 验证登录信息
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):  # 创建注册表单
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入3~30位用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': '密码长度不能低于6位'}),
                               min_length=6, max_length=30)
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}),
                                min_length=6, max_length=30)
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
                            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    def clean_username(self):  # 验证用户名
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password2(self):  # 验证密码
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('两次密码不一致,请重新输入')
        return password2

    def clean_email(self):  # 验证邮箱
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'birth']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['company', 'school', 'profession', 'address', 'about_me']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']




