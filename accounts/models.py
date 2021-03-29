from django.db import models
from django.contrib import auth

# Create your models here.

class User(auth.models.User, auth.models.PermissionsMixin):
    
    #courses = models.ManyToManyField(Course, through='UserInCourse')
    def __str__(self):
        return "@{}".format(self.username)

# class LessonPassed(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     passed = models.BooleanField(default=False)



# class CourseProgression(models.Model):
#     lessons_passed = models.ManyToManyField(to=LessonPassed)
#     current_lesson = models.PositiveIntegerField(default=1)


# class UserInCourse(models.Model):
#     user = models.ForeignKey(auth.models.User, related_name='student', on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, related_name='user_course', on_delete=models.CASCADE)
#     current_lesson = models.PositiveIntegerField(default=1)
#     lessons_passed = models.ManyToManyField(to=LessonPassed)
#     #progres = models.ForeignKey(CourseProgression, on_delete=models.CASCADE)

#     class Meta():
#         unique_together = ['user', 'course']

#     def next_lesson(self):
#         self.current_lesson += 1

    #def check_lesson(self, lesson):



