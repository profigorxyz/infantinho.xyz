from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import Teacher, Grade
from .forms import UploadFileForm
from django.contrib import messages
from openpyxl import load_workbook
import zipfile
import os
# import shutil
# from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .tasks import create_students
import pickle
from io import BytesIO
from kombu import serialization
from django.core.files import File


def loads(s):
    return pickle.load(BytesIO(s))

serialization.register(
    'my_pickle', pickle.dumps, loads,
    content_type='application/x-pickle3',
    content_encoding='binary',
)

@login_required(login_url='/login/google-oauth2/?next=/')
def update_grade(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request, 'Tem de ter\
            autorização para poder verificar presenças.')
        return render(request, 'blank.html')
    grade = Grade.objects.all()
    context = {
        'grade': grade,
    }
    return render(request, 'herd/update_grade.html', context)


@login_required(login_url='/login/google-oauth2/?next=/')
def upload_file(request):
    if request.user.email != 'prof.igor@colegioinfante.info':
        messages.error(request, 'Apenas para o prof. Igor!')
        return render(request, 'blank.html')
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if not form.is_valid():
        messages.error(request, 'Ocorreu um erro a validar.')
        return render(request, 'herd/upload.html', {'form': form})
    # form is valid:
    # with open(os.path.join(settings.MEDIA_ROOT, 'a.xlxs'), 'wb+') as f:
    #     fxlxs = File(f)
    fs = FileSystemStorage()
    fx = os.path.join(settings.MEDIA_ROOT,
                      '0' + request.FILES['xlxs'].name)
    fz = os.path.join(settings.MEDIA_ROOT,
                      '0' + request.FILES['imgzipped'].name)
    fs.save(fx, File(request.FILES['xlxs']))
    fs.save(fz, File(request.FILES['imgzipped']))
    create_students(fz, fx)
    messages.success(request, 'Ficheiros enviados com sucesso.')
    return render(request, 'herd/upload.html', {'form': form})
