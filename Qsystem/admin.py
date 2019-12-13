from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Authority)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(PaperHead)
admin.site.register(PaperBody)
admin.site.register(PaperComment)
admin.site.register(QuestionComment)
admin.site.register(UserQuestionDetail)
admin.site.register(UserPaperDetail)
