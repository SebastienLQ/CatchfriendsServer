# -*- coding: utf-8 -*
import json
import logging
import hashlib

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from serverappli.models import Profile, Friendship
from serverappli.utils import myDumpJson
from serverappli.DTO.DTO import ProfileDTO

"""
Ces fonctions concernent les utilisateurs et les profils. 
On peut créer un utilisateur, un profil, récupérer un profil, le mettre à jour, se connecter...
"""

logger = logging.getLogger(__name__)

@csrf_exempt
def createUser(request):
    """
    Créé un utilisateur de CatchFriends
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        login = objJson['login']
        email = objJson['email']
        if User.objects.filter(username=login).exists():
            return HttpResponse(content="login", status=409)
        if User.objects.filter(email=email).exists():
            return HttpResponse(content="email", status=409)
        user = User.objects.create_user(username=login, email=email, password=objJson['password'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(content="Not a POST request", status=400)


@csrf_exempt
def createProfile(request):
    """
    Créé un profil pour un utilisateur
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        description = objJson['description']
        pseudo = objJson['pseudo']
        pourcentage = objJson['pourcentage']
        Profile.objects.create_profile(user=user, description=description, pseudo=pseudo, pourcentage=pourcentage)
        logger.debug(objJson['login'] + " : profile created !")
        return HttpResponse(status=200)
    else:
        return HttpResponse(content="Not a POST request", status=400)

#@ensure_csrf_cookie
@csrf_exempt
def logUser(request):
    """
    Connecte un utilisateur
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        login = objJson['login']
        password = objJson['password']
        user = authenticate(username=login, password=password)
        if user is not None:
            if user.is_active:
                logger.debug(str(user) + " authenticated !")
                prof = Profile.objects.filter(id_user=user)[0]
                p = ProfileDTO(prof, prof.pourcentage)
                return myDumpJson(p.toJson())
            else:
                logger.error(str(user) + " is not active !")
                return HttpResponse(status=401)
        else:
            logger.error("Can't authenticate " + str(user) + "!")
            return HttpResponse(status=400)
    else:
        return HttpResponse(content="Not a POST request", status=400)

@csrf_exempt
def getProfile(request):
    """
    Récupère le profil d'un utilisateur
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])
        prof = Profile.objects.filter(id_user=user)[0]
        p = ProfileDTO(prof, prof.pourcentage)
        return myDumpJson(p.toJson())
    else:
        return HttpResponse(content="Not a POST request", status=400)



@csrf_exempt
def updateProfile(request):
    """
    Met à jour le profil d'un utilisateur
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])
        description = objJson['description']
        pseudo = objJson['pseudo']
        pourcentage = objJson['pourcentage']

        prof = Profile.objects.filter(id_user=user)[0]
        prof.description = description
        prof.pseudo = pseudo
        prof.pourcentage = pourcentage
        prof.save()

        logger.debug(objJson['login'] + " : profile updated !")
        return HttpResponse(status=200)
    else:
        return HttpResponse(content="Not a POST request", status=400)

@csrf_exempt
def getMyFriends(request):
    """
    Récupère les amis d'un utilisateur
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=objJson['login'])
        profile = Profile.objects.get(id_user=user)

        res = []
        
        friends = Friendship.objects.filter(profile1=profile)
        for friend in friends:
            p = Profile.objects.filter(pseudo=friend.profile2.pseudo)
            if p.exists():
                p = p[0]
                res.append(ProfileDTO(p, p.pourcentage).toJson())
        
        friends = Friendship.objects.filter(profile2=profile)
        for friend in friends:
            p = Profile.objects.filter(pseudo=friend.profile1.pseudo)
            if p.exists():
                p = p[0]
                res.append(ProfileDTO(p, p.pourcentage).toJson())

        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a POST request", status=400)

@csrf_exempt
def addFriend(request):
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=objJson['login'])
        profile1 = Profile.objects.filter(id_user=user)[0]
        profile2 = Profile.objects.filter(pseudo=objJson['pseudo-challenger'])[0]
        friendship = Friendship.objects.create_friendship(profile1, profile2)
        return HttpResponse(content=friendship, status=200)
    else:
        return HttpResponse(content="Not a POST request", status=400)