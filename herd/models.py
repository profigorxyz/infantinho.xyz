from django.db import models
from django.conf import settings


class Grade(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade)

    def __str__(self):
        return '{} {}'.format(self.name, self.grade.name)


class Teacher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return '{} - {} {}'.format(self.subject,
                                   self.user.first_name,
                                   self.user.last_name)


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    number = models.SmallIntegerField()
    list_number = models.SmallIntegerField()
    grade = models.ForeignKey(Grade)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['list_number']
