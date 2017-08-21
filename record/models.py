from django.db import models
from herd.models import Student, Subject


class PresRec(models.Model):
    P = 0
    F = 1
    PCHOICES = ((P, 'P'),
                (F, 'F'),
                )
    student = models.ForeignKey(Student)
    is_absent = models.SmallIntegerField(default=0, choices=PCHOICES)
    date = models.DateField()
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.get_is_absent_display()
