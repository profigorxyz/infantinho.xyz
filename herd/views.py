from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from .models import Grade, Student
from .forms import UploadFileForm


@login_required(login_url='/login/google-oauth2/?next=/')
def upload_file(request):
    if not request.user.is_staff:
        if not request.user.is_superuser:
            raise Http404
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        from openpyxl import load_workbook
        f = request.FILES['file']
        wb = load_workbook(filename=f, read_only=True)
        school = {}
        for book in wb:
            grade = book.title
            b = 1
            student = {}
            for row in book.rows:
                a = []
                for cell in row:
                    a.append(cell.value)
                student[a[0]] = [b, a[1]]
                a = []
                b += 1
            school[grade] = student
        for key in school:
            g = Grade(name=key.upper())
            g.save()
            for v in school[key]:
                st_number = v
                st_number = str(st_number).rstrip('.')
                st_order = school[key][v][0]
                st_name = school[key][v][1]
                st_name = st_name.rstrip(' ')
                f_name = st_name.split(' ', 1)[0]
                namelist = st_name.split(' ', -1)
                l_name = namelist[len(namelist) - 1]
                if User.objects.filter(username=st_number).exists():
                    continue
                else:
                    u = User.objects.create_user(
                        f_name + '_' + st_number,
                        st_number + '@colegioinfante.info',
                        'aluno' + st_number,
                    )
                    u.first_name = f_name
                    u.last_name = l_name
                    u.save()
                if Student.objects.filter(number=int(st_number)).exists():
                    continue
                else:
                    u = User.objects.filter(username=f_name + '_' + st_number)
                    g = Grade.objects.filter(name=key.upper())
                    s = Student(
                        user=u[0],
                        number=st_number,
                        list_number=st_order,
                        grade=g[0],
                    )
                    s.save()
        form = UploadFileForm()
        return render(request, 'herd/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'herd/upload.html', {'form': form})
