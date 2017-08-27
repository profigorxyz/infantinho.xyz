from django.db import models
from django.conf import settings
<<<<<<< HEAD
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
=======
>>>>>>> 334c8eba6362ccffb8257e3a2268669aa495068e


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
<<<<<<< HEAD
                                   self.user.first_name,
                                   self.user.last_name)
=======
                                   self.name.first_name,
                                   self.name.last_name)
>>>>>>> 334c8eba6362ccffb8257e3a2268669aa495068e


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    number = models.SmallIntegerField()
    list_number = models.SmallIntegerField()
    grade = models.ForeignKey(Grade)
<<<<<<< HEAD
    photo = StdImageField(null=True,
                          blank=True,
                          upload_to=UploadToUUID(path='students'),
                          variations={'face': (300, 300)})

    def __str__(self):
        return '{} {}'.format(self.user.first_name,
                              self.user.last_name)
=======

    def __str__(self):
        return '{} {}'.format(self.name.first_name, self.name.last_name)
>>>>>>> 334c8eba6362ccffb8257e3a2268669aa495068e

    class Meta:
        ordering = ['list_number']
