# -*- coding: utf-8 -*
import random
import json
import urllib
import hashlib
import codecs
import logging

from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.models import User

from serverappli.models import Profile, Theme, Category, Tag, Checkin, Profile, Question, Game, Friendship
from serverappli.utils import myDumpJson, defineCompatibility, isGoodTagName, getThemeOfTag, getCategoryOfTag
from serverappli.tagFunctions import getDataBase, getTags, addTags, findTag
from serverappli.checkinFunctions import checkDistanceBetweenCheckins
from serverappli.DTO.DTO import CategoryDTO

logger = logging.getLogger(__name__)

def getAllThemes(request):
    """
    Récupère tous les thèmes de l'application
    """
    if request.method == 'GET':
        allThemes = Theme.objects.all()
        res = []
        for theme in allThemes:
            res.append(theme.theme)
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

def getCategories(request, theme):
    """
    Récupère toutes les catégories d'un thème
    """
    if request.method == 'GET':
        them = Theme.objects.filter(theme=urllib.parse.unquote(theme))
        allCategories = Category.objects.filter(id_theme=them)

        res = []
        for cat in allCategories:
            c = CategoryDTO(cat)
            res.append(c.toJson())
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def getAllTags(request, theme, category):
    """
    Récupère tous les tags d'une catégorie d'un thème
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        name = objJson['login']
        user = User.objects.filter(username=name)
        profile = Profile.objects.filter(id_user=user)[0]
        them = Theme.objects.filter(theme=urllib.parse.unquote(theme))
        cat = Category.objects.filter(id_theme=them, category=urllib.parse.unquote(category))
        return myDumpJson(getTags(category=cat, profile=profile))
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def getTagsLetter(request, theme, category):
    """
    Récupère tous les tags d'une catégorie d'un thème, en fonction d'une recherche
    """
    if request.method == 'POST':
        letter = request.POST.get('letter')
        name = request.POST.get('login')
        user = User.objects.filter(username=name)
        them = Theme.objects.filter(theme=urllib.parse.unquote(theme))
        cat = Category.objects.filter(id_theme=them, category=urllib.parse.unquote(category))
        return myDumpJson(getTags(category=cat, profile=profile, letter=letter))
    else:
        return HttpResponse(content="Not a good request", status=400)

def dispatchDataBase(request, username):
    """
    Récupère toute la base de données
    """
    if request.method == 'GET':
        user = User.objects.filter(username=username)
        profile = Profile.objects.filter(id_user=user[0])
        res = getDataBase(profile[0])
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def dispachAddTags(request):
    """
    Ajoute un tag à un profil
    """
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        name = objJson["login"]
        user = User.objects.filter(username=name)[0]
        profile = Profile.objects.filter(id_user=user)[0]
        addTags(objJson["tags"], profile)
        return HttpResponse(status=200)
    else:
        return HttpResponse(content="Not a good request", status=400)

@ensure_csrf_cookie
def simpleGet(request):
    """
    Récupère le jeton csrf
    """
    return HttpResponse(content="Hello", status=200)

""" -------------------------------------------------------------- TESTS -------------------------------------------------------------- """

def test(request):
    didi = Profile.objects.filter(pseudo="Le didi")[0]
    zozo = Profile.objects.filter(pseudo="Zozo")[0]
    game = Game.objects.filter(profile1=zozo, profile2=didi)[0]
    questions = Question.objects.filter(id_game=game).delete()
    return myDumpJson(Question.objects.filter(id_game=game))

def test2(request):
    # friendships = Friendship.objects.all()
    # profiles = Profile.objects.all()
    # games = Game.objects.all()
    categories = Category.objects.all()
    # prof = Profile.objects.filter(pseudo="pseudo-toto")[0]
    # prof.avatar = "http://www.gravatar.com/avatar/50810029edcdaa02043eff094e4d37c6.jpg?d=identicon"
    # prof.save()
    # prof = Profile.objects.filter(pseudo="pseudo-tata")[0]
    # prof.avatar = "http://www.gravatar.com/avatar/73078069406610cd85857798e4ca6afa.jpg?d=identicon"
    # prof.save()
    # prof = Profile.objects.filter(pseudo="pseudo-titi")[0]
    # prof.avatar = "http://www.gravatar.com/avatar/04c54e28ab63ff8d332015e85fca589e.jpg?d=identicon"
    # prof.save()
    return HttpResponse(categories)

def gravatar(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if email is None:
            email = 'toto@toto.com'
        return HttpResponse(hashlib.md5(email.encode("utf-8")).hexdigest())