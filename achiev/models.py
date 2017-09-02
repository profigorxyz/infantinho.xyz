from django.db import models
from herd.models import Student


class SubSubArea(models.Model):
    ssarea = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.ssarea)


class SubArea(models.Model):
    sarea = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.sarea)


class Area(models.Model):
    AREAS = (
        (0, 'Matemática'),
        (1, 'Português'),
        (2, 'Estudo do Meio'),
    )
    area = models.SmallIntegerField(
        choices=AREAS,
        default=0,
        verbose_name='Áreas do Conhecimento',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.area)


class AreaSubareaSubSubarea(models.Model):
    area = models.ForeignKey(Area)
    sarea = models.ForeignKey(SubArea, blank=True)
    ssarea = models.ForeignKey(SubSubArea, blank=True)

    def __str__(self):
        return '{}: {!s}: {!s}: '.format(
            self.area.get_area_display(),
            self.sarea.sarea if self.sarea.sarea is not None else '_',
            self.ssarea.ssarea if self.ssarea.ssarea is not None else '_'
        )


class Achiev(models.Model):
    name = models.TextField()
    asss = models.ForeignKey(AreaSubareaSubSubarea)
    level = models.SmallIntegerField()

    def __str__(self):
        return '{}{}'.format(self.asss, self.name)


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
