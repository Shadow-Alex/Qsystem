from django.db import models


# Create your models here.
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    identification = (
        ('admin', '管理员'),
        ('student', '学生'),
        ('teacher', '老师'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    auth = models.CharField(max_length=32, choices=identification, default='学生')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
