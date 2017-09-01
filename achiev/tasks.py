from __future__ import absolute_import, unicode_literals
from celery import task, shared_task, group
from .models import Achiev, Area, SubArea, SubSubArea
from openpyxl import load_workbook
import time
import os


@task(name="create_achiev")
def create_achiev(xlxs):
    build_achiev.delay(xlxs)


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
    subarea = achiev.get('subarea')
    subsubarea = achiev.get('subsubarea')
    level = achiev.get('level')
    if not Area.objects.filter(name__exact=area):
        arobj = Area(name=area)
        arobj.save()
    else:
        arobj = Area.objects.get(name=area)
    if not SubArea.objects.filter(name__exact=subarea):
        sbobj = SubArea(name=subarea, area=arobj)
        sbobj.save()
    else:
        sbobj = SubArea.objects.get(name=subarea)
    if not SubSubArea.objects.filter(name__exact=subsubarea):
        ssbobj = SubSubArea(name=subsubarea, subarea=sbobj)
        ssbobj.save()
    else:
        ssbobj = SubSubArea.objects.get(name=subsubarea)
    if not Achiev.objects.filter(name__exact=ach_name):
        a = Achiev(
            name=ach_name,
            subsubarea=ssbobj,
            level=level,
        )
        a.save()
