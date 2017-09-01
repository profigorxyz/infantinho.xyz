from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teacher, Grade
from .forms import UploadFileForm
from django.contrib import messages
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .tasks import create_students
from django.core.files import File


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
    if not request.POST:
        return render(request, 'herd/upload.html', {'form': form})
    if not form.is_valid():
        messages.error(request, 'Ocorreu um erro a validar.')
        return render(request, 'herd/upload.html', {'form': form})
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
