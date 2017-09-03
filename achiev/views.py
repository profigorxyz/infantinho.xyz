from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UploadAchiev
from herd.models import Teacher, Subject, Student
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .tasks import create_achiev
from django.core.files import File
import os


@login_required(login_url='/login/google-oauth2/?next=/')
def upload_achiev(request):  # Create
    if request.user.email != 'prof.igor@colegioinfante.info':
        messages.error(request, 'Apenas para o prof. Igor!')
        return render(request, 'blank.html')
    form = UploadAchiev(request.POST or None, request.FILES or None)
    if not request.POST:
        return render(request, 'herd/upload.html', {'form': form})
    if not form.is_valid():
        messages.error(request, 'Ocorreu um erro a validar.')
        return render(request, 'herd/upload.html', {'form': form})
    fs = FileSystemStorage()
    fx = os.path.join(settings.MEDIA_ROOT,
                      '0' + request.FILES['xlxs'].name)
    fs.save(fx, File(request.FILES['xlxs']))
    create_achiev.delay(fx)
    messages.success(request, 'Ficheiros enviados com sucesso.')
    return render(request, 'herd/upload.html', {'form': form})


@login_required(login_url='/login/google-oauth2/?next=/')
def read_achiev(request):
    areas = {
        '0': {
            'id': 0,
            'area': 'Matemática'
        },
        '1': {
            'id': 1,
            'area': 'Português'
        },
        '2': {
            'id': 2,
            'area': 'Estudo do Meio'
        }
    }
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if teacher:
        subject = Subject.objects.filter(teacher__user=request.user.id)
        grades = [{str(v): v} for v in subject.values('grade')]
        raise
    context = {
        'grades': grades,
        'areas': areas,
    }
    return render(request, 'achiev/read_skill.html', context)


@login_required(login_url='/login/google-oauth2/?next=/')
def evaluate_achiev(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request, 'Tem de ter\
            autorização para poder verificar presenças.')
        return render(request, 'blank.html')
    subject = Subject.objects.filter(teacher__user=request.user.id)
    context = {
        'subject': subject,
    }
    return render(request, 'record/read_pres.html', context)
