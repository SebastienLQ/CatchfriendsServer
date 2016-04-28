# -*- coding: utf-8 -*
import json
import re
import logging

from datetime import datetime

from django.http import HttpResponse
from django.db import transaction

from serverappli.models import Tag, ListTags, Profile, Checkin

jsonContentType = "application/json;charset=utf-8"
voyelles = ["a", "e", "i", "o", "u", "y"]
consonnes = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","z"]
api_giant_bomb = "96ac526e5c75cac64b5822abe8a298b0fb9f9ef1"

themesStyle = {}
themesStyle["Cinéma"] = {"Color":"calm", "Icon":"ion-film-marker"}
themesStyle["Jeux-Vidéo"] = {"Color":"dark", "Icon":"ion-mouse"}
themesStyle["Musique"] = {"Color":"royal", "Icon":"ion-music-note"}
themesStyle["Nourriture"] = {"Color":"energized", "Icon":"ion-pizza"}
themesStyle["Sport"] = {"Color":"balanced", "Icon":"ion-ios-football"}

logger = logging.getLogger(__name__)

def myDumpJson(dict, status=200):
    dumped = json.dumps(dict, sort_keys=True)
    return HttpResponse(dumped, content_type=jsonContentType, status=status)

def getCategoryOfTag(tag):
    category = tag.id_category
    return category

def getThemeOfTag(tag):
    category = getCategoryOfTag(tag)
    theme = category.id_theme
    return theme

def getThemeOfCategory(category):
    theme = category.id_theme
    return theme

def severalInsert(dico, field, category, begin):
    cpt = 0
    with transaction.atomic():
        for i in range(begin, len(dico[field])):
            Tag.objects.create_tag(title=dico[field][i], category=category)
            if cpt == 10:
                break # Pas de return ici, sinon la transaction peut etre compromise
            cpt = cpt + 1
    return cpt

def isGoodTagName(name, precision=False):
    regex = re.compile("^[\w\s$':]{4,}$")
    if precision:
        regex2 = re.compile("^((?!vost)(?!trilogy)(?!pack)(?!collector)(?!edition)(?!porn)(?!teaser)(?!multiplayer)(?!gameplay)(?!quick look)(?!part \d+).)*$", re.IGNORECASE)
        return regex.match(name) and regex2.match(name)
    else:
        return regex.match(name)

def defineCompatibility(profile1, profile2):
    logger = logging.getLogger(__name__)

    alltags1 = [lt.id_tag for lt in ListTags.objects.filter(id_profile=profile1)]
    alltags2 = [lt.id_tag for lt in ListTags.objects.filter(id_profile=profile2)]
    n1 = round(len(alltags1) * profile1.pourcentage / 100)
    n2 = round(len(alltags2) * profile2.pourcentage / 100)
    compatibleTags = list(set(alltags1) & set(alltags2))
    finalRes = round(len(compatibleTags) * 100 / len(alltags1))
    if len(compatibleTags) >= n1 and len(compatibleTags) >= n2:
        return [True, finalRes]
    else:
        return [False, finalRes]
