import decimal
import re
from django.shortcuts import render, redirect

from Qsystem.models import *
from Qsystem.forms import *
from django.utils import timezone
from hashlib import sha256


def get_annual_yeild():
    return 0.01


def index(request):
    if request.session.get('block_message', None):
        # 显示报错信息并且之后不显示
        block_message = request.session['block_message']
        request.session['block_message'] = None
        return render(request, 'Qsystem/index.html', {'block_message': block_message})

    return render(request, 'Qsystem/index.html')


def login(request):
    if request.session.get('is_login', None):
        if request.session.get("success_reg_message", None):
            del request.session['success_reg_message']
        return redirect('Qsystem:index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            card_id = login_form.cleaned_data['card_id']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(card_Id=card_id)  # 身份证号
                if user.password == encoder(password, user.name):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id  # 用户序号
                    request.session['user_name'] = user.name  # 用户姓名
                    return redirect('Qsystem:index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'Qsystem/login.html', locals())

    login_form = UserForm()
    if request.session.get('success_reg_message', None):
        success_reg_message = request.session['success_reg_message']
        del request.session['success_reg_message']

    return render(request, 'Qsystem/login.html', locals())


def encoder(string1, string2):
    return sha256((str(sha256(string1.encode("utf-8")).hexdigest()) + string2).encode("utf-8")).hexdigest()


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("Qsystem:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            card_id = register_form.cleaned_data['card_id']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            phone = register_form.cleaned_data['phone']

            phone_reg = re.compile(r'1[345678]\d{9}')
            card_id_reg = re.compile(r'([A-Za-z](\d{6})\(\d\))|(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X|x)$')
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'Qsystem/register.html', locals())
            elif  len(password1) < 6:
                message = "密码长度不小于6位！"
                return render(request, 'Qsystem/register.html', locals())
            elif not phone_reg.match(phone):
                message = "请输入正确的手机号码！"
                return render(request, 'Qsystem/register.html', locals())
            elif not card_id_reg.match(card_id):
                message = "请输入正确的身份证号！"
                return render(request, 'Qsystem/register.html', locals())
            else:
                # 身份证末尾校验：
                check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'][sum(
                    [int(card_id[i]) * [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2][i] for i in
                     range(17)]) % 11]
                if not check_code == card_id[-1]:
                    message = "身份证校验和有误，请输入正确的身份证号！"
                    return render(request, 'Qsystem/register.html', locals())

                same_card_id_user = User.objects.filter(card_Id=card_id)
                if same_card_id_user:  # 身份号只能开一个账户！
                    message = '该身份证已经注册，请直接登陆！'
                    return render(request, 'Qsystem/register.html', locals())

                new_user = User.objects.create(
                    name=username,
                    password=encoder(password1, username),
                    card_Id=card_id,
                    phone=phone,
                    money=0,
                )

                # success
                request.session['success_reg_message'] = "注册成功,请直接登陆！"
                return redirect('Qsystem:login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'Qsystem/register.html', locals())


def logout(request):
    if not request.session['is_login']:
        return redirect("Qsystem:index")
    request.session.flush()
    return redirect('Qsystem:index')


def info(request):
    """账户信息"""
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    money = user.money  # 当前余额
    logs = Log.objects.filter(customer=user).order_by("-time")

    if request.session.get('success_message', None):
        success_message = request.session['success_message']
        del request.session['success_message']

    return render(request, 'Qsystem/info.html', locals())


def deposit(request):
    """存款界面"""
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')

    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        message = "无效金额！"
        if deposit_form.is_valid():
            # 结算利息、存入金额、生成Logs
            # 寻找上次利息结算时间
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            logs = Log.objects.filter(customer_id=user_id).order_by('-time')
            now = timezone.now()
            money = user.money
            deposit_amount = deposit_form.cleaned_data['amount'] * 100

            if deposit_amount <= 0:
                message = "请输入合法的金额！"
                return render(request, 'Qsystem/deposit.html', locals())
            if deposit_amount >= 100000000000000:
                message = "输入金额过大，请输入正确的金额！"
                return render(request, 'Qsystem/deposit.html', locals())

            if logs:
                lastlog = logs[0]
                lasttime = lastlog.time
                period = (now - lasttime).seconds
                current_yeild = get_annual_yeild() * (period) / (365 * 86400)
                balance_amount = round(decimal.Decimal(current_yeild) * money, 4)

                user.money += balance_amount
                user.save()
                new_log = Log.objects.create(
                    amount=balance_amount,
                    action=Log.balance,
                    customer=user,
                    left=user.money)

            user.money += deposit_amount
            user.save()
            new_log = Log.objects.create(
                amount=deposit_amount,
                action=Log.deposit,
                customer=user,
                left=user.money)

            # success!
            request.session['success_message'] = "存款成功！"
            return redirect('Qsystem:info')
    deposit_form = DepositForm()
    return render(request, 'Qsystem/deposit.html', locals())


def withdraw(request):
    """取款界面"""
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')

    if request.method == 'POST':
        withdraw_form = WithdrawForm(request.POST)
        message = "无效金额！"
        if withdraw_form.is_valid():
            # 结算利息、存入金额、生成Logs
            # 寻找上次利息结算时间
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            logs = Log.objects.filter(customer_id=user_id).order_by('-time')
            now = timezone.now()
            money = user.money
            withdraw_amount = withdraw_form.cleaned_data['amount'] * 100

            if withdraw_amount <= 0:
                message = "请输入合法的金额！"
                return render(request, 'Qsystem/withdraw.html', locals())
            if money < withdraw_amount:
                message = "账户余额不足，您账户余额为" + str(money) + "元！"
                return render(request, 'Qsystem/withdraw.html', locals())
            if logs:
                lastlog = logs[0]
                lasttime = lastlog.time
                period = (now - lasttime).seconds
                current_yeild = get_annual_yeild() * (period) / (365 * 86400)
                balance_amount = round(decimal.Decimal(current_yeild) * money, 4)

                user.money += balance_amount
                user.save()
                new_log = Log.objects.create(
                    amount=balance_amount,
                    action=Log.balance,
                    customer=user,
                    left=user.money)

            user.money -= withdraw_amount
            user.save()
            new_log = Log.objects.create(
                amount=withdraw_amount,
                action=Log.withdraw,
                customer=user,
                left=user.money)

            # success!
            request.session['success_message'] = "取款成功！"
            return redirect('Qsystem:info')
    withdraw_form = WithdrawForm()
    return render(request, 'Qsystem/withdraw.html', locals())
