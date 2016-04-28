# -*- coding: utf-8 -*
import json
import logging
from datetime import datetime
from haversine import haversine

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.models import User
from math import radians, cos, sin, asin, sqrt

from serverappli.models import Checkin, Profile, Game
from serverappli.utils import myDumpJson, defineCompatibility
from serverappli.DTO.DTO import ValidCheckinsDTO, HistoriqueCheckinDTO

@csrf_exempt
def createCheckin(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        latitude = objJson['latitude']
        longitude = objJson['longitude']
        now = datetime.now()
        previous = Checkin.objects.filter(id_user=user, latitude=latitude, longitude=longitude, date=now)
        if not previous.exists():
            checkin = Checkin.objects.create_checkin(user=user, latitude=latitude, longitude=longitude, date=now)
            logger.debug(objJson['login'] + " : " + str(checkin) + " saved !")

        return HttpResponse(status=200)
    else:
        return HttpResponse(content="Not a POST request", status=400)

def checkDistanceBetweenCheckins(firstCheckin, secondCheckin):
    res = haversine((firstCheckin.latitude, firstCheckin.longitude), (secondCheckin.latitude, secondCheckin.longitude))
    return res <= 1 # en kilomètres

def checkOneDayDifferenceBetweenDates(firstDate, secondDate):
    if firstDate < secondDate:
        delta = secondDate - firstDate
    else:
        delta = firstDate - secondDate
    return delta.days <= 1 and delta.seconds <= 86400

def findValidCheckins(user, checkin):
    logger = logging.getLogger(__name__)
    if checkin == 0:
        return []
    other_users = User.objects.exclude(username=user.username)
    myprofile = Profile.objects.filter(id_user=user)[0]
    res = []
    for u in other_users:
        checkins = list(Checkin.objects.filter(id_user=u))
        for c in checkins:
            if (checkDistanceBetweenCheckins(checkin, c) and
                checkOneDayDifferenceBetweenDates(checkin.date, c.date)):
                prof = Profile.objects.filter(id_user=u)[0]
                compatibility1 = defineCompatibility(myprofile, prof)
                compatibility2 = defineCompatibility(prof, myprofile)
                if (Game.objects.filter(profile1=myprofile, profile2=prof).exists() or
                    Game.objects.filter(profile1=prof, profile2=myprofile).exists()):
                    break
                if compatibility1[0] and compatibility2[0] :
                    vc = ValidCheckinsDTO(prof, checkin, compatibility1[1])
                    res.append(vc.toJson())
                    break
    return res

def getLastCheckin(user):
    res = Checkin.objects.filter(id_user=user).order_by("-date")
    if len(res) > 0:
        return res[0]
    return 0


def getHistoriqueCheckin(request, user):
    user = User.objects.filter(username=user)[0]
    checkins = Checkin.objects.filter(id_user=user)
    res = []
    for c in checkins:
        hc = HistoriqueCheckinDTO(c)
        res.append(hc.toJson())
    return myDumpJson(res)
