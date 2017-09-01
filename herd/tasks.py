from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from django.contrib.auth.models import User
from .models import Student, Grade
from openpyxl import load_workbook
import zipfile
import os
import glob
import shutil
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@shared_task
def build_school(x):
    wb = load_workbook(
        filename=x,
        read_only=True
    )
    for book in wb:
        ngrade = '{}'.format(book.title).upper()
        b = 1
        grades = {}
        grades[ngrade] = {}
        for row in book.rows:
            grades[ngrade]['{}'.format(row[0].value).rstrip('.')] = {
                'number': '{}'.format(row[0].value).rstrip('.'),
                'list_number': b,
                'name': row[1].value
            }
            b += 1
        [pop_student.delay(grades[ngrade][v], ngrade) for v in grades[ngrade]]
        for s in grades[ngrade]:
            try:
                student_number = int(grades[ngrade][s].get('number'))
            except ValueError:
                continue
            student = Student.objects.filter(
                number__exact=student_number).first()
            if '{}'.format(str(student_number)) not in grades[ngrade]:
                student.grade = Grade.objects.filter(name__exact='EX').first()
                student.save()
            print('Aluno {} criado ou atualizado.'.format(s))
    files = glob.glob('{}0*.*'.format(settings.MEDIA_ROOT))
    for f in files:
        os.remove(f)


@shared_task
def pop_student(x, y):
    student = x
    grade = y
    if not Grade.objects.filter(name__exact=grade).exists():
        gobj = Grade(name=grade)
        gobj.save()
    else:
        gobj = Grade.objects.get(name=grade)
    fs = FileSystemStorage()
    st_name = student.get('name')
    if not st_name:
        return 0
    st_name = st_name.rstrip(' ')
    f_name = st_name.split(' ', 1)[0]
    namelist = st_name.split(' ', -1)
    l_name = namelist[len(namelist) - 1]
    st_number = student.get('number')
    username = '{}_{}'.format(f_name, student.get('number'))
    if not User.objects.filter(username__exact=username).exists():
        u = User.objects.create_user(
            username,
            st_number + '@colegioinfante.info',
            'aluno' + st_number,
        )
        u.first_name = f_name
        u.last_name = l_name
        u.save()
    else:
        u = User.objects.get(username=username)
    fname = '{}.jpg'.format(st_number)
    try:
        fimg = fs.open(fname, mode='rb')
    except FileNotFoundError:
        default = '{}'.format(os.path.join(settings.MEDIA_ROOT,
                                           'default.jpg'))
        shutil.copy(default, os.path.join(settings.MEDIA_ROOT, fname))
        fimg = fs.open(fname, mode='rb')
    f = ImageFile(fimg)
    if not Student.objects.filter(number__exact=int(st_number)).exists():
        s = Student(
            user=u,
            number=int(st_number),
            list_number=student.get('list_number'),
            grade=gobj,
            photo=f,
        )
        s.save()
    else:
        s = Student.objects.get(number=int(st_number))
        s.grade = gobj
        s.photo = f
        s.save()
    fimg.close()
    f.close()
    files = glob.glob('{}{}*.jpg'.format(settings.MEDIA_ROOT, fname))
    for f in files:
        os.remove(f)


@task(name="create_students")
def create_students(fzip, xlsx):
    fjpg = zipfile.ZipFile(fzip, 'r')
    fjpg.extractall(settings.MEDIA_ROOT)
    build_school.delay(xlsx)
