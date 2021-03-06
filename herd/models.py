from django.db import models
from django.conf import settings
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID


class Grade(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)
    grade = models.ManyToManyField(Grade)
    club = models.NullBooleanField()

    def __str__(self):
        grade = [n.get('name') for n in self.grade.values('name')]
        grade = ''.join(grade)
        return '{} {}'.format(self.name, grade)


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
    photo = StdImageField(null=True,
                          blank=True,
                          upload_to=UploadToUUID(path='students'),
                          variations={'face': (300, 300)})
    club = models.ManyToManyField(Subject,
                                  blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name,
                              self.user.last_name)

    class Meta:
        ordering = ['list_number']
