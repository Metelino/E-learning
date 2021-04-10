from django.db import models
from django.contrib import auth
from courses.models import Course, Node
from annoying.fields import AutoOneToOneField

# Create your models here.

class User(auth.models.User, auth.models.PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)

class Profile(models.Model):
    LEARNING_TYPE = [
        ('0', 'Wzrokowiec'),
        ('1', 'Dzidowiec'),
        ('2', 'Słuchowiec'),
    ]
    user = AutoOneToOneField(auth.models.User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    courses = models.ManyToManyField(Course)
    learning_type = models.CharField(choices=LEARNING_TYPE, default='0', max_length=30)
    nodes_passed = models.ManyToManyField(Node)

    def is_in_course(self, course):
        return self.courses.filter(pk=course.pk).exists()
    #lessons_passed = models.ManyToManyField(Node)

# class UserInCourse(models.Model):
#     user = models.ForeignKey(Profile, related_name='student', on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, related_name='student_course', on_delete=models.CASCADE)
#     nodes_passed = models.ManyToManyField(Node)

#     class Meta():
#         unique_together = ['user', 'course']




