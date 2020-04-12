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

    card_Id = models.CharField(max_length=128, default='N/A')  # TODO：加入unique限制！
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    phone = models.CharField(max_length=128, default='N/A')
    money = models.DecimalField(max_digits=20, decimal_places=4, default=0)  # 余额

    def __str__(self):
        return self.name


class Log(models.Model):
    """流水"""
    """包含两种情形，一种为用户主动存款、取款结余；另一种为利息结算"""
    withdraw = '1'
    deposit = '2'
    balance = '3'
    transaction = (
        (withdraw, '取款'),
        (deposit, '存款'),
        (balance, '结余'),
    )
    time = models.DateTimeField(auto_now_add=True)  # Timestamped created when log is written.
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=32, choices=transaction, default='取款')
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    left = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return self.customer.name + "    " + self.action + "    " + str(self.amount)