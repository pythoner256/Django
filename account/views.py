from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserInfoForm, UserForm, UserProfileForm
from .models import UserInfo, UserProfile


def blog_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(reverse('blog_list'))
    else:
        login_form = LoginForm()
    return render(request, 'account/login.html', {'login_form': login_form})


def blog_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password=password2)
            user.save()
            UserProfile.objects.create(user=user)
            UserInfo.objects.create(user=user)
            auth.login(request, user=user)
            # return render(request,'blog/index.html',{'username': username})
            return redirect(reverse('blog_list'))
    else:
        register_form = RegisterForm()
    return render(request, 'account/register.html', {'register_form': register_form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('blog_list'))


@login_required(login_url='account/login')  # 判断用户是否登录，没有登录就跳转到登录页面
def myself(request):
    user = User.objects.get(username=request.user.username)
    userporfile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    context = {}
    context['user'] = user
    context['userinfo'] = userinfo
    context['userprofile'] = userporfile
    return render(request, 'account/myself.html', context)


@login_required(login_url='account/login')
def edit_myself(request):
    context = {}
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    userprofile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        userprofileform = UserProfileForm(request.POST)
        userinfoform = UserInfoForm(request.POST)
        userform = UserForm(request.POST)
        if userinfoform.is_valid()*userprofileform.is_valid()*userform.is_valid():
            user.email = userform['email']
            userinfo.school = userinfoform.cleaned_data['school']
            userinfo.profession = userinfoform.cleaned_data['profession']
            userinfo.address = userinfoform.cleaned_data['address']
            userinfo.company = userinfoform.cleaned_data['company']
            userinfo.about_me = userinfoform.cleaned_data['about_me']
            userprofile.phone = userprofileform.cleaned_data['phone']
            userprofile.birth = userprofileform.cleaned_data['birth']
            userinfo.save()
            userprofile.save()
            userprofile.save()
            return redirect(reverse('account:myself'))
    else:
        userform = UserForm(instance=request.user)
        userprofileform = UserProfileForm(initial={'birth': userprofile.birth,
                                                   'phone': userprofile.phone})
        userinfoform = UserInfoForm(initial={'school': userinfo.school,
                                             'address': userinfo.address,
                                             'company': userinfo.company,
                                             'about_me': userinfo.about_me,
                                             'profession': userinfo.profession})
        context['userinfoform'] = userinfoform
        context['userprofileform'] = userprofileform
        context['userform'] = userform
        return render(request, 'account/edit_myself.html', context)



