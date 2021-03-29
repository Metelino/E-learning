from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Course)
admin.site.register(models.Lesson)
admin.site.register(models.Test)
admin.site.register(models.NodeInCourse)
admin.site.register(models.LessonFile)