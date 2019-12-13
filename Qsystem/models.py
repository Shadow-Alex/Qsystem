import datetime
from django.db import models

# Create your models here.
from django.utils import timezone


class Authority(models.Model):
    """身份->权限"""
    admin = 'admin'
    student = 'student'
    teacher = 'teacher'
    identification = (
        (admin, '管理员'),
        (student, '学生'),  # 不可以出题
        (teacher, '老师'),
    )

    auth = models.CharField(max_length=32, choices=identification, default='学生')
    access_to_assign = models.BooleanField(default=False)

    def __str__(self):
        return self.auth


class User(models.Model):
    """用户"""
    male = 'male'
    female = 'female'
    gender = (
        (male, '男'),
        (female, '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL, null=True)
    complete = models.ManyToManyField('Question', through='UserQuestionDetail')

    def __str__(self):
        return self.name


class Question(models.Model):
    """题目"""
    options = (
        ('A', "A"),
        ('B', "B"),
        ('C', 'C'),
        ('D', 'D'),
    )

    question_text = models.CharField(max_length=256)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 人走了题目留下
    correct_option = models.CharField(max_length=10, choices=options, default='A')
    A_text = models.CharField(max_length=256, default="请输入选项")
    B_text = models.CharField(max_length=256, default="请输入选项")
    C_text = models.CharField(max_length=256, default="请输入选项")
    D_text = models.CharField(max_length=256, default="请输入选项")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class PaperHead(models.Model):
    """试卷头部"""
    paper_title = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 人走了试卷留下
    question = models.ManyToManyField('Question', through='PaperBody')  # 试卷m：n题目

    def __str__(self):
        return self.paper_title


class PaperBody(models.Model):
    """试卷主体：试卷头部与题目的多对多关系"""
    paper_head = models.ForeignKey(PaperHead, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.paper_head) + "\tinclude\t" + str(self.question)


class PaperComment(models.Model):
    """试卷评论"""
    comment_topic = models.CharField(max_length=256, default="请输入标题")
    comment_text = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    paper_head = models.ForeignKey(PaperHead, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.__str__() + ":  " + self.comment_text


class QuestionComment(models.Model):
    """题目评论"""
    comment_topic = models.CharField(max_length=256, default="请输入标题")
    comment_text = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.author.__str__() + ":  " + self.comment_text


class UserQuestionDetail(models.Model):
    """用户做题记录"""
    options = (
        ('A', "A"),
        ('B', "B"),
        ('C', 'C'),
        ('D', 'D'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateField('date answered')
    inPaper = models.ForeignKey('UserPaperDetail', default=None, on_delete=models.CASCADE,
                                null=True, blank=True, db_constraint=False)  # 做题记录并不一定是做试卷时产生的,None代表不是
    option = models.CharField(max_length=32, choices=options, default='A')  # 单选题
    is_correct = models.BooleanField(default=True)  # 是否是正确的，额外数据方便统计查找。

    def __str__(self):
        if self.inPaper is None:
            return str(self.user) + " complete " + str(self.question) + " @ " + str(self.date) + " by accident."
        else:
            return str(self.user) + " complete " + str(self.question) + " @ " + str(self.date) + " in Paper No." + str(
                self.inPaper)


class UserPaperDetail(models.Model):
    """用户做试卷记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(PaperHead, on_delete=models.CASCADE)
    date = models.DateField('date finished')

    def __str__(self):
        return str(self.user) + " complete " + str(self.paper) + " @ " + str(self.date)


class UpQuestionComment(models.Model):
    """用户点赞记录"""
    question_comment = models.ForeignKey(QuestionComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField('date finished')

    def __str__(self):
        return str(self.user) + "up" + str(self.question_comment) + " @ " + str(self.date)