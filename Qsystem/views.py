from django.shortcuts import render

# Create your views here.
# Qsystem/views.py

from django.shortcuts import render, redirect

from Qsystem.models import *
from Qsystem.forms import *
from django.utils import timezone


def index(request):
    pass
    return render(request, 'Qsystem/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('Qsystem:index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('Qsystem:index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'Qsystem/login.html', locals())

    login_form = UserForm()
    return render(request, 'Qsystem/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("Qsystem:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'Qsystem/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'Qsystem/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'Qsystem/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('Qsystem:login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'Qsystem/register.html', locals())


def logout(request):
    if not request.session['is_login']:
        return redirect("Qsystem:index")
    request.session.flush()
    return redirect('Qsystem:index')


def base(request):
    return render(request, 'Qsystem/base.html')


def assignQuestion(request):
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        message = "请检查填写的内容！"
        if question_form.is_valid():  # 获取数据
            pass  # 判断出题合理性，暂时想不到什么要求。

            # 创建新问题
            new_question = Question.objects.create(
                pub_date=timezone.now(),
                question_text=question_form.cleaned_data['question_text'],
                A_text=question_form.cleaned_data['A_text'],
                B_text=question_form.cleaned_data['B_text'],
                C_text=question_form.cleaned_data['C_text'],
                D_text=question_form.cleaned_data['D_text'],
                correct_option=question_form.cleaned_data['correctOption'],
            )
            # 增加对象关联 : Question n <--author--> 1 User
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            user.question_set.add(new_question)

            return redirect('Qsystem:index')  # 后续可以加入继续出题或者成功提示！
    question_form = QuestionForm()
    return render(request, 'Qsystem/assignQuestion.html', {"Question_form": question_form})


def assignPaperHead(request):
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')
    if request.method == 'POST':
        paper_form = PaperHeadForm(request.POST)
        message = "请检查填写的内容！"
        if paper_form.is_valid():
            pass
            # 创建 PaperHead
            new_paperHead = PaperHead.objects.create(
                paper_title=paper_form.cleaned_data['paperTitle'],
            )
            # 增加对象联系 : paperHead n <--author--> 1 User
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            user.paperhead_set.add(new_paperHead)

            return redirect('Qsystem:index')

    paper_form = PaperHeadForm()
    return render(request, 'Qsystem/assignPaperHead.html', {'PaperHead_form': paper_form})


def test(request):
    return render(request, 'Qsystem/test.html')


def questionDetail(request, question_id):  # 做题页面
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')
    if request.method == 'POST':
        option = request.POST.get('option', None)
        message = "请检查填写内容！"
        if option is not None:
            # userQuestionDetail n <--产生--> 1 User.
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            # userQuestionDetail n <--属于--> 1 Question.
            question = Question.objects.get(id=question_id)
            # 创建做题记录
            new_userQuestionDetail = UserQuestionDetail.objects.create(
                date=timezone.now(),
                option=option,
                user=user,
                question=question,
                inPaper=None,  # 顺序做题遇到的
                is_correct=(option == question.correct_option),
            )
            # TODO 返回结果页
            pass
            return redirect('Qsystem:index')
    question = Question.objects.get(id=question_id)
    return render(request, 'Qsystem/questionDetail.html', locals())


def questionList(request):
    question_list = Question.objects.order_by('-pub_date')
    return render(request, 'Qsystem/questionList.html', locals())


def questionOverview(request, question_id):
    if not request.session.get('is_login', None):
        return redirect('Qsystem:index')
    # 查找所有人做题记录
    question = Question.objects.get(id=question_id)
    total_attempt = question.userquestiondetail_set.count()
    correct_attempt = question.userquestiondetail_set.filter(is_correct=True).count()
    # 查找用户做题记录
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    user_attempt = user.userquestiondetail_set.filter(question_id=question_id).order_by('-date')
    # 查找所有题解，按照likes排序。
    comments = question.questioncomment_set.order_by('-likes')
    return render(request, 'Qsystem/questionOverview.html', locals())


def questionComment(request, questionComment_id):
    Comment = QuestionComment.objects.get(id=questionComment_id)
    return render(request, 'Qsystem/questionComment.html', locals())
