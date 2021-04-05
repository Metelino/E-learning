from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Course)
admin.site.register(models.Node)
admin.site.register(models.LessonFile)
admin.site.register(models.Question)
admin.site.register(models.Answer)