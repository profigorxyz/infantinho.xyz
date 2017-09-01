from django.db import models
from herd.models import Student


class Area(models.Model):
    AREAS = (
        (0, 'Matemática'),
        (1, 'Português'),
        (2, 'Estudo do Meio'),
    )
    name = models.SmallIntegerField(
        choices=AREAS,
        default=0,
        verbose_name='Áreas do Conhecimento'
    )

    def __str__(self):
        return '{}'.format(self.name)


class SubArea(models.Model):
    area = models.ForeignKey(Area, default=1)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class SubSubArea(models.Model):
    subarea = models.ForeignKey(SubArea, default=1)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Achiev(models.Model):
    name = models.TextField()
    subsubarea = models.ForeignKey(SubSubArea)
    level = models.SmallIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.subsubarea.subarea.area, self.name)


class StudentSysLevel(models.Model):
    """docstring for StudentSysLevel"""
    AVAL = (
        (0, 'Ainda não tentei.'),
        (1, 'Consigo com a ajuda do professor.'),
        (2, 'Consigo com a ajuda de um amigo.'),
        (3, 'Consigo sozinho.'),
        (4, 'Sou capaz de ajudar um amigo.'),
    )
    student = models.ForeignKey(Student)
    achiev = models.ForeignKey(Achiev, verbose_name='competência')
    student_level = models.SmallIntegerField(
        choices=AVAL,
        default=0,
        verbose_name=''
    )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{0} = {1}'.format(self.achiev, self.student_level)
