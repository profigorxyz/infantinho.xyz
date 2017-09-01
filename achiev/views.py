from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UploadAchiev
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .tasks import create_achiev
from django.core.files import File
import os


@login_required(login_url='/login/google-oauth2/?next=/')
def upload_achiev(request):
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
