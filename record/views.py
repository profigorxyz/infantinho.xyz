# TODO construir uma loading bar para quando está a carregar a tabela
# e ou a construir os ficheiros para download
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from herd.models import Teacher, Subject, Student
from .forms import PresForm
from .models import PresRec


@login_required(login_url='/login/google-oauth2/?next=/')
def pres_create(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request,
                       'Tem de ter autorização para poder marcar presenças.')
        return render(request, 'blank.html')
    form = PresForm()
    subject = Subject.objects.filter(teacher__user=request.user.id)
    context = {
        'form': form,
        'subject': subject,
    }
    if request.method == 'POST':
        subject = Subject.objects.get(id=request.POST['subject'])
        grade = [i.get('pk') for i in subject.grade.values('pk')]
        if subject.club is True:
            students = Student.objects.filter(club=subject.id)
        else:
            students = Student.objects.filter(
                grade__in=grade
            )
        date = request.POST['date_submit'].split('\'')[0]
        for student in students:
            try:
                if request.POST[str(student.id)]:
                    absent = 1
            except KeyError:
                absent = 0
            p = PresRec(
                student=student,
                is_absent=absent,
                subject=subject,
                date=date,
            )
            p.save()
        messages.success(request,
                         'Presenças de {} marcadas para o dia {}.'.format(
                             subject,
                             date))
    return render(request, 'record/create_pres.html', context)


@login_required(login_url='/login/google-oauth2/?next=/')
def pres_read(request):
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


@login_required(login_url='/login/google-oauth2/?next=/')
def pres_print(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request, 'Tem de ter\
            autorização para poder verificar presenças.')
        return render(request, 'blank.html')
    subject = Subject.objects.filter(teacher__user=request.user.id)
    context = {
        'subject': subject,
    }
    return render(request, 'record/print_pres.html', context)


@login_required(login_url='/login/google-oauth2/?next=/')
def create_proj(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        student = Student.objects.filter(user__exact=request.user.id).first()
        if not student:
            messages.error(request, 'Tem de ter \
                        autorização para criar um projeto.')
            return render(request, 'blank.html')
    context = {
    }
    if request.method == 'POST':
        return 0
    return render(request, 'record/create_proj.html', context)

    # if now.month < 3:
    #     end_month = datetime.date(now.year, 7, 1)
    #     start_date = datetime.date(now.year - 1, 9, 1)
    # else:
    #     end_date = datetime.date(now.year + 1, 7, 1)
    #     start_date = datetime.date(now.year, 9, 1)


#     if request.method == 'POST' and request.POST['stage'] == '1':
#         import datetime
#         from openpyxl import workbook, load_workbook
#         from openpyxl.drawing.image import Image
# #        from openpyxl.drawing.image import Image // implementar logo
#         flpres = open(os.path.join(LOCAL_FILES, 'presence.xlsx'), 'rb')
#         wb = load_workbook(flpres)
#         ws = wb['PRES']
#         now = datetime.datetime.now()
#         if now.month < 7:
#             end_date = datetime.date(now.year, 7, 1)
#             start_date = datetime.date(now.year - 1, 9, 1)
#         else:
#             end_date = datetime.date(now.year + 1, 7, 1)
#             start_date = datetime.date(now.year, 9, 1)
#         p = Presence.objects.filter(
#                                    subject__exact=int(request.POST['subject']),
#                                    date__range=(start_date, end_date)
#                                    ).order_by('-date')

#         def gotx(day):
#             switcher = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "H", 7: "I", 8: "J", 9: "K", 10: "L", 11: "M", 12: "N",
#                                 13: "O", 14: "P", 15: "Q", 16: "R", 17: "S", 18: "T", 19: "U", 20: "V", 21: "W", 22: "X", 23: "Y", 24: "Z",
#                                 25: "AA", 26: "AB", 27: "AC", 28: "AD", 29: "AE", 30: "AF", 31: "AG"}
#             return switcher.get(day)

#         def goty(counter,month):
#             y = 56 + (counter * 10)
#             if month > 8 and month < 13:
#                 y = y + counter + (month - 7)
#             else:
#                 y = y + counter + month + 5
#             return str(y)
#         gsub = Subject.objects.get(id=request.POST['subject'])
#         students = Student.objects.filter(grade__exact=gsub.grade)
#         for student in students:
#             ws['A' + goty(student.list_number-1, 9)] = '{} {}'.format(student.name.first_name, student.name.last_name)
#         for p in p:
#             if p.is_absent == 0:
#                 pres = 'P'
#             elif p.is_absent == 1:
#                 pres = 'F'
#             ws[gotx(p.date.day) + goty(
#                                          p.student.list_number-1,
#                                          p.date.month)] = pres
#         ws = wb['PRES']
#         fllogo = open(os.path.join(LOCAL_FILES, 'logotipo.png'), 'rb')
#         img = Image(fllogo)
#         ws.add_image(img, 'L3')
#         ws['A22'] = '{}'.format(gsub.name)
#         ws['A27'] = '{}'.format(gsub.grade.name)
#         ws['A44']  = '{} {} / {}'.format('Ano letivo de ', start_date.year, end_date.year)
#         wb.save('{}/{}_{}.xlsx'.format(LOCAL_FILES, gsub.name, gsub.grade.name))
#         subject = Subject.objects.all()
#         return render(request, 'record/report.html', {
#                   'errors': errors,
#                   'subject': subject,
#                   })
#     else:
#         subject = Subject.objects.all()
#         return render(request, 'record/report.html', {
#                   'errors': errors,
#                   'subject': subject,
#                   })


# @login_required(login_url='/login/google-oauth2/?next=/')
# def registry(request):
#     try:
#         teacher = Teacher.objects.filter(name__exact=request.user.id).first()
#     except:
#         teacher = None
#     if teacher:
#         context = {
#             'teacher': teacher,
#         }
#         return render(request, 'record/entrypoint.html', context)
#     else:
#         context = {
#         }
#         return render(request, 'record/entrypoint.html', context)
#     return render(request, 'blank.html')


# @login_required(login_url='/login/google-oauth2/?next=/')
# def print_report(request):
#     teacher = Teacher.objects.filter(name__exact=request.user.id).first()
#     if not teacher:
#         messages.error(request, 'Tem de ter autorização para poder verificar as presenças.')
#         return render(request, 'blank.html')
#     subject = Subject.objects.filter(teacher__name=request.user.id)
#     form = PrintDateForm(request.POST or None)
#     if form.is_valid():
#         grade = int(request.POST['subject'].split("-")[1])
#         subject = int(request.POST['subject'].split("-")[0])
#         students = Student.objects.filter(grade__exact=grade)
#         teacher = Teacher.objects.filter(name__exact=request.user.id, subject__exact=int(request.POST['subject'].split("-")[0])).first()
#         printout = {}
#         for student in students:
#             pres = Presence.objects.filter(
#                 subject__exact=subject,
#                 student__name__exact=student.name,
#                 date__range=[
#                     request.POST['initialdate'],
#                     request.POST['finaldate']
#                 ],
#                 is_absent=0
#             ).count()
#             absent = Presence.objects.filter(
#                 subject__exact=subject,
#                 student__name__exact=student.name,
#                 date__range=[
#                     request.POST['initialdate'],
#                     request.POST['finaldate']
#                 ],
#                 is_absent=1
#             ).count()
#             printout[student.list_number] = {
#                 'name': '{} {}'.format(
#                     student.name.first_name,
#                     student.name.last_name
#                 ),
#                 'presents': pres,
#                 'absents': absent,
#             }
#         context = {
#             'teacher': teacher,
#             'initialdate': request.POST['initialdate'],
#             'finaldate': request.POST['finaldate'],
#             'subject': subject,
#             'print': sorted(printout.items()),
#         }
#         return render(request, 'record/print.html', context)
#     context = {
#         'subject': subject,
#         'form': form,
#     }
#     return render(request, 'record/printform.html', context)
