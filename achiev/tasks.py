from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from .models import Achiev, Area, SubArea, SubSubArea
from .models import AreaSubareaSubSubarea as ASSS
from openpyxl import load_workbook
import os


@task(name="erase_trash")
def erase_trash(path_to_file):
    os.remove(path_to_file)


@task(name="create_achiev")
def create_achiev(xlxs):
    build_achiev(xlxs)


@shared_task
def build_achiev(xlsx):
    wb = load_workbook(
        filename=xlsx,
        read_only=True
    )
    for book in wb:
        narea = int(book.title)
        achievs = {}
        achievs[narea] = {}
        anumber = 1
        for row in book.rows:
            achievs[narea]['{}'.format(anumber)] = {
                'subarea': '{}'.format(row[0].value).title().rstrip(),
                'subsubarea': '{}'.format(row[2].value).title().rstrip(),
                'level': '{}'.format(row[1].value).title().rstrip(),
                'name': '{}'.format(row[3].value).rstrip(),
            }
            anumber += 1
        [pop_achiev.delay(achievs[narea][v], narea) for v in achievs[narea]]


@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def pop_achiev(x, y):
    achiev = x
    area = y
    ach_name = achiev.get('name')
    sarea = achiev.get('subarea')
    ssarea = achiev.get('subsubarea')
    level = achiev.get('level')
    if not SubSubArea.objects.filter(ssarea__exact=ssarea):
        ssarea = SubSubArea(ssarea=ssarea)
        ssarea.save()
    else:
        ssarea = SubSubArea.objects.filter(ssarea=ssarea).first()
    if not SubArea.objects.filter(sarea__exact=sarea):
        sarea = SubArea(sarea=sarea)
        sarea.save()
    else:
        sarea = SubArea.objects.get(sarea=sarea)
    if not Area.objects.filter(area__exact=area):
        area = Area(area=area)
        area.save()
    else:
        area = Area.objects.filter(area=area).first()
    if not ASSS.objects.filter(area__exact=area,
                               sarea__exact=sarea,
                               ssarea__exact=ssarea):
        asss = ASSS(
            area=area,
            sarea=sarea,
            ssarea=ssarea
        )
        asss.save()
    else:
        asss = ASSS.objects.filter(area__exact=area,
                                   sarea__exact=sarea,
                                   ssarea__exact=ssarea).first()
    if not Achiev.objects.filter(name__exact=ach_name,
                                 asss__exact=asss):
        a = Achiev(
            name=ach_name,
            asss=asss,
            level=level,
        )
        a.save()
