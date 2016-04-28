# -*- coding: utf-8 -*
import datetime
import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from serverappli.models import Profile, Theme, Category, Tag, ListTags
from serverappli.utils import myDumpJson, getCategoryOfTag, getThemeOfTag, getThemeOfCategory

logger = logging.getLogger(__name__)

@csrf_exempt
def getCurrentTags(request):
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        profile = Profile.objects.filter(id_user=user)
        listtags = ListTags.objects.filter(id_profile=profile)
        
        res = {}
        if len(listtags) > 0:
            for lt in listtags:
                tag = lt.id_tag
                category = tag.id_category
                theme = category.id_theme
                if not theme.theme in res:
                    res[theme.theme] = {}
                if not category.category in res[theme.theme]:
                    res[theme.theme][category.category] = []
                res[theme.theme][category.category].append(tag.tag)
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def getAskableCurrentTags(request):
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        asked = objJson['asked']
        user = User.objects.filter(username=objJson['login'])[0]
        profile = Profile.objects.filter(id_user=user)[0]
        listtags = ListTags.objects.filter(id_profile=profile)

        res = {}
        if len(listtags) > 0:
            for lt in listtags:
                tag = lt.id_tag
                category = tag.id_category
                theme = category.id_theme
                if (theme.theme in asked 
                    and category.category in asked[theme.theme] 
                    and tag.tag in asked[theme.theme][category.category]):
                    continue
                if not theme.theme in res:
                    res[theme.theme] = {}
                if not category.category in res[theme.theme]:
                    res[theme.theme][category.category] = []
                res[theme.theme][category.category].append(tag.tag)
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

def getTags(category, profile, letter=None):
    logger = logging.getLogger(__name__)
    if letter is None:

        allTags = Tag.objects.filter(id_category=category)
    else:
        regex = r'^' + letter + ".*$"
        allTags = Tag.objects.filter(id_category=category, tag__iregex=regex)

    res = {}
    for tag in allTags:
        lt = ListTags.objects.filter(id_profile=profile, id_tag=tag)
        if len(lt) == 0:
            res[tag.tag] = False
        else:
            res[tag.tag] = True
    return res

def getDataBase(profile):
    logger = logging.getLogger(__name__)
    allTags = Tag.objects.all()
    res = {}
    for tag in allTags:
        theme = getThemeOfTag(tag)
        category = getCategoryOfTag(tag)
        if not theme.theme in res:
            res[theme.theme] = {}

        if not category.category in res[theme.theme]:
            res[theme.theme][category.category] = {}

        lt = ListTags.objects.filter(id_profile=profile, id_tag=tag)

        if len(lt) == 0:
            res[theme.theme][category.category][tag.tag] = False
        else:
            res[theme.theme][category.category][tag.tag] = True
    return res

def findTag(theme, category, tag):
    th = Theme.objects.filter(theme=theme)
    cat = Category.objects.filter(category=category, id_theme=th)
    ta = Tag.objects.filter(id_category=cat, tag=tag)
    return ta[0]

def addTags(json, profile):
    logger = logging.getLogger(__name__)
    now = datetime.datetime.now()
    for obj in json:
        tag = findTag(obj["Theme"], obj["Category"], obj["Tag"])
        if (obj["Added"]):
            lt = ListTags.objects.create_listTags(profile, tag, now)
            lt.save()
        else:
            lt = ListTags.objects.filter(id_profile=profile, id_tag=tag)
            lt.delete()