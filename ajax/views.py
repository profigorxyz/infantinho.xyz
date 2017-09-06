import os
import datetime
from text_unidecode import unidecode
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage, DefaultStorage
from django.db.models import Sum, Count
from django.core.files.base import ContentFile
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from herd.models import Teacher, Subject, Student, Grade
from achiev.models import StudentSysLevel, Achiev, AreaSubareaSubSubarea, \
    Area, SubArea
from record.models import PresRec


def build_students(**kwargs):
    grade = kwargs.get('grade', None)
    subject = kwargs.get('subject', None)
    if not grade and not subject:
        return 0
    if not grade:
        sub = Subject.objects.filter(pk__exact=subject).first()
        grade = Grade.objects.filter(pk__exact=sub.grade_id).first()
    sts = Student.objects.filter(
        grade__exact=grade).order_by('user__first_name', 'user__last_name')
    data = {}
    data['team'] = {}
    data['students'] = {}
    first = True
    for student in sts:
        if first:
            first = False
            data['team']['grade'] = student.grade_id
            data['team']['subject'] = subject
            data['team']['name'] = student.grade.name
        name = '{}'.format(student.number)
        data['students'][name] = {
            'id': student.id,
            'name': '{}'.format(student).upper(),
            'jpg': student.photo.face.url,
        }
    return data


def get_x(day):
    switcher = {
        1: "C",
        2: "D",
        3: "E",
        4: "F",
        5: "G",
        6: "H",
        7: "I",
        8: "J",
        9: "K",
        10: "L",
        11: "M",
        12: "N",
        13: "O",
        14: "P",
        15: "Q",
        16: "R",
        17: "S",
        18: "T",
        19: "U",
        20: "V",
        21: "W",
        22: "X",
        23: "Y",
        24: "Z",
        25: "AA",
        26: "AB",
        27: "AC",
        28: "AD",
        29: "AE",
        30: "AF",
        31: "AG"
    }
    return switcher.get(day)


def get_y(counter, month):
    y = 90 + (counter * 10)
    if month > 8 and month < 13:
        y = y + counter + (month - 7)
    else:
        y = y + counter + month + 5
    return str(y)


@login_required(login_url='/login/google-oauth2/?next=/')
def get_print_url(request):
    subject = int(request.GET.get('subject', None))
    if not subject:
        messages.error(request,
                       'Tem de escolher uma turma.')
        return render(request, 'blank.html')
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request,
                       'Tem de ter autorização para aceder.')
        return render(request, 'blank.html')
    storage = DefaultStorage()
    flpres = storage.open('presence.xlsx', mode='rb')
    wb = load_workbook(flpres)
    ws = wb['Folha1']
    now = datetime.datetime.now()
    if now.month < 7:
        end_date = datetime.date(now.year, 7, 1)
        start_date = datetime.date(now.year - 1, 9, 1)
    else:
        end_date = datetime.date(now.year + 1, 7, 1)
        start_date = datetime.date(now.year, 9, 1)
    p = PresRec.objects.filter(
        subject__exact=subject,
        date__range=(start_date, end_date)
    ).order_by('-date')
    subject = Subject.objects.get(pk__exact=subject)
    grade = Grade.objects.get(pk__exact=subject.grade.pk)
    students = Student.objects.filter(
        grade__exact=grade).order_by('user__first_name', 'user__last_name')
    for student in students:
        ws['A' + get_y(student.list_number - 1, 9)] = '{} {}'.format(
            student.user.first_name, student.user.last_name)
    for p in p:
        if p.is_absent == 0:
            pres = 'P'
        elif p.is_absent == 1:
            pres = 'F'
        ws[get_x(p.date.day) + get_y(
            p.student.list_number - 1,
            p.date.month)] = pres
    ws = wb['Folha1']
    fllogo = storage.open('logotipo.png', mode='rb')
    img = Image(fllogo)
    ws.add_image(img, 'L3')
    ws['A35'] = '{}'.format(subject)
    ws['A62'] = '{} {} / {}'.format(
        'Ano letivo de ', start_date.year, end_date.year)
    filename = ''.join('{}.xlsx'.format(subject).split())
    fs = FileSystemStorage()
    fs = fs.open(filename, mode='wb+')
    # This dont work properly
    # fs = storage.open('print/{}'.format(filename), mode='wb+')
    # fs = ContentFile()
    wb.save(fs)
    storage.save(filename, fs)
    fs.close()
    fllogo.close()
    flpres.close()
    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
    file_url = storage.url(filename)
    data = []
    data.append({
        'url': file_url,
        'name': '{}'.format(filename).upper(),
    })
    return JsonResponse(data, safe=False)


@login_required(login_url='/login/google-oauth2/?next=/')
def get_students(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request,
                       'Tem de ter autorização para aceder.')
        return render(request, 'blank.html')
    grade = request.GET.get('grade', None)
    subject = request.GET.get('subject', None)
    if not grade:
        sub = Subject.objects.filter(pk__exact=subject).first()
        grade = Grade.objects.filter(pk__exact=sub.grade_id).first()
    idata = build_students(grade=grade, subject=subject)
    allgd = Grade.objects.all()
    grades = {}
    for agd in allgd:
        grades[agd.name] = {
            'id': agd.id,
            'name': agd.name,
        }
    data = {
        'grade': grades,
        'student': idata['students'],
        'class': idata['team'],
    }
    jsondump = {
        'sort_keys': True,
    }
    return JsonResponse(data, json_dumps_params=jsondump)


@login_required(login_url='/login/google-oauth2/?next=/')
def get_presents(request):
    teacher = Teacher.objects.filter(user__exact=request.user.id).first()
    if not teacher:
        messages.error(request,
                       'Tem de ter autorização para aceder.')
        return render(request, 'blank.html')
    subject = request.GET.get('subject', None)
    subject = Subject.objects.get(pk__exact=subject)
    grade = Grade.objects.get(pk__exact=subject.grade.pk)
    students = Student.objects.filter(
        grade__exact=grade).order_by('user__first_name', 'user__last_name')
    subjtitle = str(subject)
    now = datetime.datetime.now()
    if now.month < 12 and now.month > 8:
        start_date = datetime.date(now.year, 9, 1)
        end_date = datetime.date(now.year, now.month, now.day)
    elif now.month < 3:
        start_date = datetime.date(now.year - 1, now.month - 3, 1)
        end_date = datetime.date(now.year, now.month, now.day)
    elif now.month > 6:
        start_date = datetime.date(now.year, 4, 1)
        end_date = datetime.date(now.year, 6, 30)
    else:
        start_date = datetime.date(now.year, now.month - 3, 1)
        end_date = datetime.date(now.year, now.month, now.day)
    studic = []
    for student in students:
        pres = PresRec.objects.filter(
            subject__exact=subject,
            student__user__exact=student.user,
            date__range=[
                start_date,
                end_date
            ],
            is_absent=0).count()
        absent = PresRec.objects.filter(
            subject__exact=subject,
            student__user__exact=student.user,
            date__range=[
                start_date,
                end_date
            ],
            is_absent=1).count()
        studic.append({
                      'name': '{}'.format(student),
                      'pres': pres,
                      'absent': absent,
                      'start_date': start_date,
                      'end_date': end_date,
                      'subject': subjtitle
                      }
                      )
    data = studic
    return JsonResponse(data, safe=False)


def get_xp(**kwargs):
    # student, area, sarea, ssarea, achiev
    student = kwargs.get('student', None)
    area = kwargs.get('area', None)
    sarea = kwargs.get('sarea', None)
    ssarea = kwargs.get('ssarea', None)
    achiev = kwargs.get('achiev', None)
    if not student:
        if not area and not sarea and not ssarea:
            return int(Achiev.objects.
                       aggregate(c=Count('id')).
                       get('c') * 4)
        if not sarea and not ssarea:
            return int(
                Achiev.objects.
                filter(asss__in=[
                    v.get('id')
                    for v in
                    AreaSubareaSubSubarea.objects.filter(area=area).
                    values('id')
                ]).
                aggregate(c=Count('id')).
                get('c') * 4)
        if not ssarea:
            return int(
                Achiev.objects.
                filter(asss__in=[
                    v.get('id')
                    for v in
                    AreaSubareaSubSubarea.objects.filter(sarea=sarea).
                    values('id')
                ]).
                aggregate(c=Count('id')).
                get('c') * 4)
        return int(
            Achiev.objects.
            filter(asss__in=[
                v.get('id')
                for v in
                AreaSubareaSubSubarea.objects.filter(ssarea=ssarea).
                values('id')
            ]).
            aggregate(c=Count('id')).
            get('c') * 4)
    qssl = StudentSysLevel.objects.filter(student=student)
    if achiev:
        a = qssl.filter(achiev=achiev).first()
        return 0 if a is None else int(a.student_level or 0)
    if not area and not sarea and not ssarea:
        return int(
            qssl.aggregate(s=Sum('student_level')).
            get('s') or 0)
    if not sarea and not ssarea:
        return int(
            qssl.
            filter(achiev__in=[
                v.get('id')
                for v in
                Achiev.objects.filter(asss__in=[
                    x.get('id')
                    for x in
                    AreaSubareaSubSubarea.objects.filter(area=area).
                    values('id')
                ]).values('id')
            ]).
            aggregate(s=Sum('student_level')).
            get('s') or 0)
    if not ssarea:
        return int(
            qssl.
            filter(achiev__in=[
                v.get('id')
                for v in
                Achiev.objects.filter(asss__in=[
                    x.get('id')
                    for x in
                    AreaSubareaSubSubarea.objects.filter(sarea=sarea).
                    values('id')
                ]).values('id')
            ]).
            aggregate(s=Sum('student_level')).
            get('s') or 0)
    return int(
        qssl.
        filter(achiev__in=[
            v.get('id')
            for v in
            Achiev.objects.filter(asss__in=[
                x.get('id')
                for x in
                AreaSubareaSubSubarea.objects.filter(ssarea=ssarea).
                values('id')
            ]).values('id')
        ]).
        aggregate(s=Sum('student_level')).
        get('s') or 0)


def build_achiev(**kwargs):
    # level, area, sarea, ssarea
    level = kwargs.get('level', None)
    area = kwargs.get('area', None)
    sarea = kwargs.get('sarea', None)
    ssarea = kwargs.get('ssarea', None)
    if not level:
        return Achiev.objects.all()
    if not area:
        return Achiev.objects.filter(
            level=level
        ).distinct().values('asss__area__id')
    if not sarea:
        return Achiev.objects.filter(level=level, asss__in=[
            v.get('id')
            for v in
            AreaSubareaSubSubarea.objects.filter(area=area).
            order_by('sarea', 'ssarea').
            values('id')
        ]).distinct().values(
            'asss__sarea',
            'asss__sarea__sarea',
        )
    if not ssarea:
        if AreaSubareaSubSubarea.objects.filter(
            sarea=sarea
        ).first().ssarea.__str__() != 'None':
            return Achiev.objects.filter(
                level=level
            ).distinct().values(
                'asss__ssarea',
                'asss__ssarea__ssarea',
            )
        return Achiev.objects.filter(level=level, asss__in=[
            v.get('id')
            for v in
            AreaSubareaSubSubarea.objects.filter(sarea=sarea).
            order_by('sarea', 'ssarea').
            values('id')
        ]).values('id', 'name')
    return Achiev.objects.filter(level=level, asss__in=[
        v.get('id')
        for v in
        AreaSubareaSubSubarea.objects.filter(ssarea=ssarea).
        order_by('sarea', 'ssarea').
        values('id')
    ]).values('id', 'name')


def get_achiev(**kwargs):
    # student, area, sarea, ssarea, achiev
    level = kwargs.get('level', None)
    student = kwargs.get('student', None)
    grade = kwargs.get('grade', None)
    area = kwargs.get('area', None)
    sarea = kwargs.get('sarea', None)
    ssarea = kwargs.get('ssarea', None)
    jsondump = {
        'sort_keys': True,
    }
    data = {}
    if grade:
        idata = build_students(grade=grade)
        data = {}
        for student in list(idata['students']):
            student_id = idata['students'][student].get('id')
            student_name = idata['students'][student].get('name')
            data[student] = {
                'name': student_name,
                'xp': get_xp(student=student_id),
            }
            for area in list(build_achiev(level=level)):
                area_id = area.get('asss__area__id')
                data[student][str(area_id)] = {
                    'id': area_id,
                    'name': Area.objects.get(id=area_id).get_area_display(),
                    'xp': get_xp(
                        student=student_id,
                        area=area_id),
                }
        return JsonResponse(data, json_dumps_params=jsondump)
    if student:
        if not sarea:
            for a in list(build_achiev(level=level, area=area)):
                sarea_id = a.get('asss__sarea')
                sarea_name = a.get('asss__sarea__sarea')
                data[sarea_id] = {
                    'name': sarea_name,
                    'xp': get_xp(student=student, sarea=sarea_id),
                    'max_xp': get_xp(sarea=sarea_id)
                }
            return JsonResponse(data, json_dumps_params=jsondump)
        if not ssarea:
            if AreaSubareaSubSubarea.objects.filter(
                sarea=sarea
            ).first().ssarea.__str__() == 'None':
                for a in list(
                    build_achiev(level=level, area=area, sarea=sarea)
                ):
                    achiev_id = a.get('id')
                    achiev_name = a.get('name')
                    data[str(achiev_id)] = {
                        'name': achiev_name,
                        'xp': get_xp(student=student, achiev=achiev_id),
                        'max_xp': 4
                    }
                return JsonResponse(data, json_dumps_params=jsondump)
            for a in list(build_achiev(level=level, area=area, sarea=sarea)):
                if str(a.get('asss__ssarea__ssarea')) == 'None':
                    continue
                ssarea_id = a.get('asss__ssarea')
                ssarea_name = a.get('asss__ssarea__ssarea')
                data[ssarea_id] = {
                    'name': ssarea_name,
                    'xp': get_xp(student=student, ssarea=ssarea_id),
                    'max_xp': get_xp(ssarea=ssarea_id)
                }
            return JsonResponse(data, json_dumps_params=jsondump)
        for a in list(build_achiev(
            level=level,
            area=area,
            sarea=sarea,
            ssarea=ssarea)
        ):
            achiev_id = a.get('id')
            achiev_name = a.get('name')
            data[str(achiev_id)] = {
                'name': achiev_name,
                'xp': get_xp(student=student, achiev=achiev_id),
                'max_xp': 4
            }
        return JsonResponse(data, json_dumps_params=jsondump)
    return 0


    # qg = Grade.objects.filter(id__exact=grade).first()
    # qs = Student.objects.filter(grade__exact=qg).order_by(
    #     'user__first_name', 'user__last_name', 'list_number')
    # qa = Area.objects.all()
    # # points = {} This should be part of data
    # # data: {
    # #     $student_id$: {
    # #         sudent_name: str,
    # #         points: int
    # #         areas: {
    # #             points: int,
    # #             $area_id$: {
    # #                 points: int,
    # #                 area_name: str,
    # #                 sub_area_id: {
    # #                     sarea_name: str,
    # #                     points: int,
    # #                     achiev_id: {
    # #                         achiev_name: str,
    # #                         points: int
    # #                     }
    # #                     sub_sub_area_id: {
    # #                         sub_sub_area_name: str,
    # #                         points: int,
    # #                         achievs: {
    # #                             achiev_id: {
    # #                                 achiev_name: str,
    # #                                 points: int
    # # }   }   }   }   }   }   }   }
    # data = {}  # Dictionary to return with
    # for s in qs:
    #     qssl = StudentSysLevel.objects.filter(student=s)
    #     data[str(s.id)] = {
    #         'student_name': s.user.get_full_name(),
    #         'points_own': int(
    #             qssl.agregate(Sum('student_level')).
    #             get('student_level__sum') or 0),
    #         'points_total': int(),
    #         'areas': {}
    #     }
    #     for na in list(v.get('id') for v in qa.values('id')):
    #         data[s.id]['areas'][str(na)] = {
    #             'points_own': int(),
    #             'points_total': int(),
    #             'area_name': qa.get(id=na).get_area_display()
    #         }
    #         asss = AreaSubareaSubSubarea.objects.filter(area__id=na)
    #         for ns in list(v.get('sarea_id')
    #                        for v in asss.distinct().values('sarea_id')):
    #             qach = Achiev.objects.filter(
    #                 asss__in=list(v.get('id') for v in asss.filter(
    #                     sarea_id=ns).values('id')))
    #             data[s.id]['areas'][str(na)][str(ns)] = {
    #                 'points_own': int(),
    #                 'points_total': int(),
    #                 'sarea_name': str(asss.filter(sarea__id=ns).first().sarea)
    #             }
    #             for v in qach.values('id'):
    #                 data[s.id]['areas'][str(na)][str(ns)][str(v.get('id'))] = {
    #                     'achiev_name': str(qach.get(id=v.get('id')).name),
    #                     'points_own': int(),
    #                     'points_total': int()
    #                 }
    #             for nss in list(v.get('ssarea_id')
    #                             for v in asss.
    #                             filter(sarea=ns).
    #                             values('ssarea_id')):
    #                 qach = Achiev.objects.filter(
    #                     asss__in=list(v.get('id') for v in asss.filter(
    #                         ssarea_id=nss).values('id')))
    #                 data[s.id]['areas'][str(na)][str(ns)][str(nss)] = {
    #                     'points_own': int(),
    #                     'points_total': int(),
    #                     'ssarea_name': str(asss.
    #                                        filter(ssarea__id=nss).
    #                                        first().ssarea)
    #                 }
    #                 for v in qach.values('id'):
    #                     data[s.id]['areas'][str(
    #                         na
    #                     )][str(
    #                         ns
    #                     )][str(
    #                         nss
    #                     )][str(v.get('id'))] = {
    #                         'achiev_name': str(qach.get(id=v.get('id')).name),
    #                         'points_own': int(),
    #                         'points_total': int()
    #                     }
    # return data


