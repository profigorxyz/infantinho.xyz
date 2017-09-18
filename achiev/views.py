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
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if teacher:
        subject = Subject.objects.filter(
            teacher__user=request.user.id
        ).order_by('grade__name')
        grades = list()
        [grades.append({'id': subject[n].grade_id,
                        'grade': str(subject[n].grade)}
                       )
            for n in range(subject.count())]
        teacher = 1
    else:
        grades = None
    n = [n for n in range(23)]
    student = Student.objects.filter(user__exact=request.user.id).first()
    context = {
        'is_student': student,
        'is_teacher': teacher,
        'grades': grades,
        'range': n,
    }
    return render(request, 'achiev/read_achiev.html', context)


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
