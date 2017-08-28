from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Teacher, Subject, Student, Grade
from .forms import UploadFileForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage, DefaultStorage


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
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request, 'Tem de ter\
            autorização para poder verificar presenças.')
        return render(request, 'blank.html')
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        from openpyxl import load_workbook
        f = request.FILES['file']
        wb = load_workbook(filename=f, read_only=True)
        school = {}
        for book in wb:
            grade = '{}'.format(book.title).upper()
            b = 1
            school[grade] = {}
            for row in book.rows:
                school[grade]['{}'.format(row[0].value).rstrip('.')] = {
                    'list_number': b,
                    'name': row[1].value
                }
                b += 1
        for grade in school:
            if not Grade.objects.filter(name__exact=grade).exists():
                gobj = Grade(name=grade)
                gobj.save()
            else:
                gobj = Grade.objects.get(name=grade)
            for student in school[grade]:
                st_name = school[grade][student].get('name')
                if not st_name:
                    continue
                st_name = st_name.rstrip(' ')
                f_name = st_name.split(' ', 1)[0]
                namelist = st_name.split(' ', -1)
                l_name = namelist[len(namelist) - 1]
                username = '{}_{}'.format(f_name, student)
                if not User.objects.filter(username__exact=username).exists():
                    u = User.objects.create_user(
                        username,
                        student + '@colegioinfante.info',
                        'aluno' + student,
                    )
                    u.first_name = f_name
                    u.last_name = l_name
                    u.save()
                else:
                    u = User.objects.get(username=username)
                storage = DefaultStorage()
                f = 'alunos/{}.jpg'.format(student)
                f = storage.open(f, mode='rb')
                if not Student.objects.filter(number__exact=int(student)
                                              ).exists():
                    s = Student(
                        user=u,
                        number=int(student),
                        list_number=school[grade][student].get('list_number'),
                        grade=gobj,
                        photo=f,
                    )
                    s.save()
                    f.close()
                else:
                    Student.objects.get(number=int(student))
                    s.grade = gobj
                    s.photo = f
                    s.save()
                    f.close()
            g = Student.objects.filter(grade=gobj)
            for s in g:
                if '{}'.format(s.number) not in school[grade]:
                    s.grade = Grade.objects.filter(name__exact='EX').first()
                    s.save()
        form = UploadFileForm()
        return render(request, 'herd/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'herd/upload.html', {'form': form})
