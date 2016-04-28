# -*- coding: utf-8 -*
import urllib.request
import json
import pickle
import time
from string import ascii_lowercase
from datetime import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.http import HttpResponse
from serverappli.utils import isGoodTagName, severalInsert
from serverappli.tagFunctions import findTag
from serverappli.models import Theme, Category, Tag, ListTags, Profile, Checkin, Game, Question


# @transaction.atomic
def initDB():
    print(datetime.now(), "Démarrage de initDB")

    try:
        with open('dbFiles/tags.json', 'r', encoding='utf8') as data_file:
            data = json.load(data_file)
            with transaction.atomic():
                print(datetime.now(), "Load tags.json")
                for theme in data:
                    th = Theme.objects.create_theme(title=theme)
                    for category in data[theme]:
                        ca = Category.objects.create_category(title=category, theme=th)
                        for tag in data[theme][category]:
                            Tag.objects.create_tag(title=tag, category=ca)
                print(datetime.now(), "TI bruts ajoutés")
    except IOError:
        print("Le fichier tags.json n'existe pas !")

    # with open('dbFiles/jeux.pkl', 'rb') as input_file:
    #     listGames = pickle.load(input_file)
    #     gameCategory = Category.objects.filter(category="Jeu")[0]
    #     cpt = 0
    #     for tag in listGames:
    #         if (cpt % 100 == 1):
    #             time.sleep(5)
    #         Tag.objects.create_tag(title=tag, category=gameCategory)
    #     print(datetime.now(), "Jeux ajoutés", cpt)

    # with open('dbFiles/artists.pkl', 'rb') as input_file:
    #     listArtists = pickle.load(input_file)
    #     artistCategory = Category.objects.filter(category="Artiste-Groupe")[0]
    #     cpt = 0
    #     for tag in listArtists:
    #         if (cpt % 100 == 1):
    #             time.sleep(5)
    #         Tag.objects.create_tag(title=tag, category=artistCategory)
    #     print(datetime.now(), "Artistes-Groupe ajoutés", cpt)

    # with open('dbFiles/films.pkl', 'rb') as input_file:
    #     listFilms = pickle.load(input_file)
    #     filmCategory = Category.objects.filter(category="Artiste-Groupe")[0]
    #     cpt = 0
    #     for tag in listFilms:
    #         if (cpt % 100 == 1):
    #             time.sleep(5)
    #         Tag.objects.create_tag(title=tag, category=filmCategory)
    #     print(datetime.now(), "Films ajoutés", cpt)

    # try:
    #     with open('giantbomb_data.json', 'r') as data_file:
    #         print(datetime.now(), "Load giantbomb_data.json")
    #         data = json.load(data_file)
    #         gameCategory = Category.objects.filter(category="Jeu")[0]
    #         res = 0
    #         for tag in data["Jeux-Vidéo"]["Jeu"]:
    #             res = res + 1
    #             Tag.objects.create_tag(title=tag, category=gameCategory)
    #         # while res % 10 == 0:
    #         #     res = res + severalInsert(data, "games", gameCategory, res)
    #         print(datetime.now(), "Jeux ajoutés", res)
    # except IOError:
    #     print("Le fichier giantbomb_data.json n'existe pas !")

    # try:
    #     with open('itunes_data.json', 'r') as data_file:    
    #         data = json.load(data_file)
    #         cinemaFilm = Category.objects.filter(category="Film")[0]
    #         musicArtist = Category.objects.filter(category="Artiste-Groupe")[0]
    #         res = 0
    #         for tag in data["Cinéma"]["Film"]:
    #             res = res + 1
    #             Tag.objects.create_tag(title=tag, category=cinemaFilm)
    #         # while res % 10 == 0:
    #         #     res = res + severalInsert(data, "cinemaFilm", cinemaFilm, res)
    #         print(datetime.now(), "Films ajoutés", res)
    #         res = 0
    #         for tag in data["Musique"]["Artiste-Groupe"]:
    #             res = res + 1
    #             Tag.objects.create_tag(title=tag, category=musicArtist)
    #         # while res % 10 == 0:
    #         #     res = res + severalInsert(data, "musicArtist", musicArtist, res)
    #         print(datetime.now(), "Artiste-Groupe ajoutés", res)
    # except IOError:
    #     print("Le fichier itunes_data.json n'existe pas !")

    ## TEST LISTES
    with transaction.atomic():
        toto = User.objects.create_user(username="toto", email="toto@toto.com", password="toto")
        tata = User.objects.create_user(username="tata", email="tata@tata.com", password="tata")
        titi = User.objects.create_user(username="titi", email="titi@titi.com", password="titi")

        profileToto = Profile.objects.create_profile(user=toto, description="Je suis toto !", pseudo="pseudo-toto", pourcentage=25)
        profileTata = Profile.objects.create_profile(user=tata, description="Je suis tata !", pseudo="pseudo-tata", pourcentage=25)
        profileTiti = Profile.objects.create_profile(user=titi, description="Je suis titi !", pseudo="pseudo-titi", pourcentage=25)

        cinema = Theme.objects.filter(theme="Cinéma")[0]
        cinemaActor = Category.objects.filter(category="Acteur-Actrice", id_theme=cinema)[0]
        cinemaGenre = Category.objects.filter(category="Genre", id_theme=cinema)[0]
        jd = Tag.objects.filter(tag="Jean Dujardin", id_category=cinemaActor)[0]
        sj = Tag.objects.filter(tag="Scarlett Johansson", id_category=cinemaActor)[0]
        sf = Tag.objects.filter(tag="Science-Fiction", id_category=cinemaGenre)[0]

        food = Theme.objects.filter(theme="Nourriture")[0]
        foodAliment = Category.objects.filter(category="Aliment", id_theme=food)[0]
        chocolat = Tag.objects.filter(tag="Chocolat", id_category=foodAliment)[0]

        music = Theme.objects.filter(theme="Musique")[0]
        musicGenre = Category.objects.filter(category="Genre", id_theme=music)[0]
        musicArtist = Category.objects.filter(category="Artiste-Groupe", id_theme=music)[0]
        rock = Tag.objects.filter(tag="Rock", id_category=musicGenre)[0]
        electro = Tag.objects.filter(tag="Électro", id_category=musicGenre)[0]
        acdc = Tag.objects.filter(tag="ACDC", id_category=musicArtist)[0]

        rpg = findTag("Jeux-Vidéo", "Genre", "RPG")

        ListTags.objects.create_listTags(profile=profileToto, tag=rock)
        ListTags.objects.create_listTags(profile=profileToto, tag=electro)
        ListTags.objects.create_listTags(profile=profileToto, tag=rpg)
        ListTags.objects.create_listTags(profile=profileToto, tag=acdc)
        ListTags.objects.create_listTags(profile=profileToto, tag=sj)

        ListTags.objects.create_listTags(profile=profileTata, tag=jd)
        ListTags.objects.create_listTags(profile=profileTata, tag=sj)
        ListTags.objects.create_listTags(profile=profileTata, tag=sf)
        ListTags.objects.create_listTags(profile=profileTata, tag=rock)

        ListTags.objects.create_listTags(profile=profileTiti, tag=rock)
        ListTags.objects.create_listTags(profile=profileTiti, tag=electro)
        ListTags.objects.create_listTags(profile=profileTiti, tag=rpg)
        ListTags.objects.create_listTags(profile=profileTiti, tag=acdc)
        ListTags.objects.create_listTags(profile=profileTiti, tag=jd)
        ListTags.objects.create_listTags(profile=profileTiti, tag=sj)
        ListTags.objects.create_listTags(profile=profileTiti, tag=sf)

        checkin1 = Checkin.objects.create_checkin(user=toto, latitude=48.857160, longitude=2.294234)
        checkin2 = Checkin.objects.create_checkin(user=titi, latitude=48.858000, longitude=2.294500)
        checkin3 = Checkin.objects.create_checkin(user=tata, latitude=48.857805, longitude=2.295173)
        checkin4 = Checkin.objects.create_checkin(user=tata, latitude=48.858393, longitude=2.296048)
        
        farbefore = datetime(2000,1,1,0,0)
        before = datetime(2015,4,15,16,0)
        after = datetime(2015,4,15,17,0)

        game1 = Game.objects.create_game(profile1=profileTata, profile2=profileToto, startDate=datetime.now())
        question_chocolat = Question.objects.create_question(game=game1, prof_ask=profileTata, tag=chocolat, question="Aimes-tu le " + chocolat.tag + " ?")
        question_acdc = Question.objects.create_question(game=game1, question="Aimes-tu " + acdc.tag + " ?", prof_ask=profileTata, tag=acdc, askDate=after)
        question_rpg = Question.objects.create_question(game=game1, question="Aimes-tu les " + rpg.tag + " ?", prof_ask=profileTata, tag=rpg)
        question_rpg2 = Question.objects.create_question(game=game1, question="Aimes-tu les " + rpg.tag + " ?", prof_ask=profileToto, tag=rpg, askDate=before)
        question_rock = Question.objects.create_question(game=game1, question="Aimes-tu le " + rock.tag + " ?", prof_ask=profileToto, tag=rock)
        question_sj = Question.objects.create_question(game=game1, question="Es-tu fan de " + sj.tag + " ?", prof_ask=profileToto, tag=sj, askDate=farbefore)
        question_jd = Question.objects.create_question(game=game1, question="Es-tu fan de " + jd.tag + " ?", prof_ask=profileToto, tag=jd)

        game2 = Game.objects.create_game(profile1=profileToto, profile2=profileTiti, startDate=datetime.now())
        question_chocolat = Question.objects.create_question(game=game2, question="Aimes-tu le " + chocolat.tag + " ?", prof_ask=profileTiti, tag=chocolat)
        question_acdc = Question.objects.create_question(game=game2, question="Aimes-tu " + acdc.tag + " ?", prof_ask=profileTata, tag=acdc, askDate=after)

        print("Base de test initialisée")

    print(datetime.now(), "Base initialisée pour le dev !")

def clearDB():
    Profile.objects.all().delete()
    Game.objects.all().delete()
    Question.objects.all().delete()
    ListTags.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()
    Theme.objects.all().delete()
    Checkin.objects.all().delete()
    User.objects.all().delete()
    print("Base vidée !")

def itunesDB(request):
    fullsecondletter = [""] + list(ascii_lowercase)
    res = {}
    res["musicArtist"] = []
    for c1 in ascii_lowercase:
        for c2 in fullsecondletter:
            for c3 in fullsecondletter:
                url = "https://itunes.apple.com/search?term=" + c1 + c2 + c3 + "&media=music&entity=musicArtist&limit=200&sort=popular&country=fr"
                response = urllib.request.urlopen(url)
                str_response = response.readall().decode('utf-8')
                data = json.loads(str_response)['results']
                for r in data:
                    if isGoodTagName(r['artistName']):
                        res["musicArtist"].append(r['artistName'])

    res["cinemaFilm"] = []
    for c1 in ascii_lowercase:
        for c2 in fullsecondletter:
            for c3 in fullsecondletter:
                url = "http://itunes.apple.com/search?term=" + c1 + c2 + c3 + "&media=movie&entity=movie&limit=200&sort=popular&country=fr&attribute=movieTerm"
                response = urllib.request.urlopen(url)
                str_response = response.readall().decode('utf-8')
                data = json.loads(str_response)['results']
                for r in data:
                    if isGoodTagName(r['trackName'], True):
                        res["cinemaFilm"].append(r['trackName'])

    with open('itunes_data.json', 'w') as outfile:
        json.dump(res, outfile, ensure_ascii=False)
    return HttpResponse(content="Base de données Itunes récupérée", status=200)

def giantBombDB(request):
    fullsecondletter = [""] + list(ascii_lowercase)
    res = {}
    res["games"] = []
    for c1 in ascii_lowercase:
        for c2 in fullsecondletter:
            for c3 in fullsecondletter:
                url = "http://www.giantbomb.com/api/search/?api_key=96ac526e5c75cac64b5822abe8a298b0fb9f9ef1&format=json&query=%22" + c1 + c2 + c3 + "%22&field_list=name&resources=game"
                response = urllib.request.urlopen(url)
                str_response = response.readall().decode('utf-8')
                data = json.loads(str_response)['results']
                for r in data:
                    if isGoodTagName(r['name']):
                        res["game"].append(r['name'])

    with open('giantbomb_data.json', 'w') as outfile:
        json.dump(res, outfile, ensure_ascii=False)
    return HttpResponse(content="Base de données GiantBomb récupérée", status=200)

def nettoyage(request):
    if request.method == 'GET':
        clearDB()
        initDB()
        return HttpResponse(content="La base a été nettoyée et réiniitalisée pour le DEV", status=200)
    return HttpResponse(content="Ne tentez pas ce que vous ne voulez pas faire !", status=403)
    