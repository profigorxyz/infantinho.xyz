# import os
# from django.conf import settings
from django.shortcuts import render  # , redirect
# from .models import Presence
from django.contrib import messages
from student.models import Teacher  # Grade, Student, Subject, Teacher
# from django.http import Http404
# from django.core.files.storage import default_storage
from .forms import PresForm  # DateForm, PrintDateForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/google-oauth2/?next=/')
def pres_create(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request,
                       'Tem de ter autorização para poder marcar presenças.')
        return render(request, 'blank.html')
    form = PresForm()
    context = {
        'form': form,
    }
    return render(request, 'record/create_pres.html', context)

# #  Enter if its a post from the final form.
#     if request.method == 'POST' and request.POST['stage'] == '2':
#         students = Student.objects.filter(grade__exact=request.POST['grade'])
#         date = request.POST['date'].split('\'')[1]
#         for student in students:
#             p = Presence(
#                 student=student,
#                 is_absent=request.POST[str(student.user)],
#                 subject=Subject.objects.get(id=request.POST['subject']),
#                 date=date,
#             )
#             p.save()
#         stage = 0
#         messages.success(request,
#                          'Presenças do {} marcadas no dia {}.'.format(
#                              Subject.objects.get(id=request.POST['subject']),
#                              date))
#         return redirect('/pres/')
# #  Enter elif there's a subject in the POST.
#     elif "subject" in request.POST:
#         stage = 1
#         grade = int(request.POST['subject'].split("-")[1])
#         subject = int(request.POST['subject'].split("-")[0])
#         date = request.POST['date'],
#         students = Student.objects.filter(grade__exact=int(grade))
#         ngrade = Grade.objects.get(pk=grade)
#         nsubject = Subject.objects.get(pk=subject)
#         context = {
#             'grade': grade,
#             'subject': subject,
#             'ngrade': ngrade,
#             'nsubject': nsubject,
#             'stage': stage,
#             'students': students,
#             'date': date,
#         }
#         return render(request, 'record/preform.html', context)
# #  Default enter point.
#     else:
#         stage = 0
#         subject = Subject.objects.filter(teacher__name=request.user.id)
#         form = DateForm(request.POST or None)
#         context = {
#             'stage': stage,
#             'subject': subject,
#             'form': form,
#         }
#         return render(request, 'record/preform.html', context)
#     return render(request, 'blank.html')


# @login_required(login_url='/login/google-oauth2/?next=/')
# def report(request):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     errors = []  # need to implement someway to show errors.
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
