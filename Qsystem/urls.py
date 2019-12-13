from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from Qsystem import views

app_name = 'Qsystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('base/', views.base, name='base'),
    path('assignQuestion/', views.assignQuestion, name='assignQuestion'),
    path('assignPaperHead/', views.assignPaperHead, name='assignPaperHead'),
    path('question/<int:question_id>/', views.questionOverview, name='questionOverview'),  # TODO:单道题目概览
    path('question/<int:question_id>/overview/', views.questionOverview, name='questionOverview'),
    path('question/<int:question_id>/detail/', views.questionDetail, name='questionDetail'),  # TODO：单道题目详情 题目提交后返回尚未完成
    path('question/list/', views.questionList, name='questionList'),  # TODO: 题目列表
    path('question/comment/<int:questionComment_id>', views.questionComment, name='questionComment'),
    # TODO：题目对应题解页，没想好是否放到单道题目概览下面，点赞功能还没完成。
    # path('paper/<int:paper_id>/', views.paperOverview, name='paperOverview'),                       # 单份试卷预览 TODO
    # path('paper/<int:paper_id>/overview', views.paperOverview, name='paperOverview'),               # 单份试卷预览 TODO
    # path('paper/<int:paper_id>/detail', views.paperDetail, name='paperOverview'),                   # 单份试卷详情 TODO
    # path('paper/list/', views.paperList, name='paperList'),                                         # 试卷列表     TODO
    path('test/', views.test, name='test')  # 测试html
]
