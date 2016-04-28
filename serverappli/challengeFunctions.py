# -*- coding: utf-8 -*
import json
import logging

from datetime import datetime
from collections import OrderedDict

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from serverappli.models import Profile, Game, Question, Tag, ListTags, Friendship
from serverappli.checkinFunctions import findValidCheckins, getLastCheckin
from serverappli.utils import myDumpJson, defineCompatibility, getThemeOfTag
from serverappli.tagFunctions import findTag
from serverappli.DTO.DTO import QuestionDTO, ProfileDTO, CurrentGamesDTO

"""Récupère les challengers possibles"""
@csrf_exempt
def getPossibleChallengers(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        res = findValidCheckins(user, getLastCheckin(user))
        return myDumpJson(res)
    else:
        return HttpResponse(content="Not a good request", status=400)

"""Récupère les demandes de challenge"""
@csrf_exempt
def getDemandesChallenges(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        profile2 = Profile.objects.filter(id_user=user)[0]
        games = Game.objects.filter(profile2=profile2, startDate=None)
        res = []
        for g in games:
            profile1 = g.profile1
            compatibility = defineCompatibility(profile2, profile1)
            if compatibility[0] :
                dc = ProfileDTO(profile1, compatibility[1])
                res.append(dc.toJson())
        return myDumpJson(res, status=200)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def getCurrentGames(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        prof = Profile.objects.filter(id_user=user)[0]
        games = Game.objects.filter(profile2=prof).exclude(startDate=None)
        res = []
        for g in games:
            cg = CurrentGamesDTO(g.profile1, g.turn2)
            res.append(cg.toJson())
        games = Game.objects.filter(profile1=prof).exclude(startDate=None)
        for g in games:
            cg = CurrentGamesDTO(g.profile2, g.turn1)
            res.append(cg.toJson())
        return myDumpJson(res, status=200)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def getGameQuestions(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        prof = Profile.objects.filter(id_user=user)[0]
        profchall = Profile.objects.filter(pseudo=objJson['pseudo-challenger'])[0]
        
        game = Game.objects.filter(profile1=prof, profile2=profchall)
        if len(game) == 0:
            game = Game.objects.filter(profile1=profchall, profile2=prof)
        if len(game) == 0:
            game = Game.objects.create_game(profile1=prof, profile2=profchall, startDate=datetime.now())
        else:
            game = game[0]

        questions = Question.objects.filter(id_game=game)
        tab = []
        for question in questions:
            if question.prof_ask == prof:
                lt = ListTags.objects.filter(id_profile=profchall, id_tag=question.id_tag)
                q = QuestionDTO(question, len(lt) == 1, True)
            else :
                lt = ListTags.objects.filter(id_profile=prof, id_tag=question.id_tag)
                q = QuestionDTO(question, len(lt) == 1, False)            
            tab.append(q.toJson())

        res = {}
        res['questions'] = tab
        res['turn'] = game.turn1 if game.profile1 == prof else game.turn2
        res['startDate'] = game.startDate.strftime('%d/%m/%Y %H:%M:%S')
        if len(questions) > 0 :
            res['lastDate'] = questions[len(questions) - 1].askDate.strftime('%d/%m/%Y %H:%M:%S') 
        else:
            res['lastDate'] = ' - '
        f1 = Friendship.objects.filter(profile1=prof, profile2=profchall)
        f2 = Friendship.objects.filter(profile1=profchall, profile2=prof)
        res['friend'] = False
        res['canBeFriends'] = False

        if f1.exists() or f2.exists():
            res['friend'] = True
        else:
            num = 0
            challNum = 0
            for q in res['questions']:
                if q['answer']:
                    if q['profile'] == profchall:
                        challNum += 1
                    if q['profile'] == prof:
                        num += 1
            res['canBeFriends'] = num >= 3 and challNum >= 3
        return myDumpJson(res, status=200)
    else:
        return HttpResponse(content="Not a good request", status=400)

@csrf_exempt
def addQuestion(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        objJson = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=objJson['login'])[0]
        prof = Profile.objects.filter(id_user=user)[0]
        profchall = Profile.objects.filter(pseudo=objJson['pseudo-challenger'])[0]
        game = Game.objects.filter(profile1=prof, profile2=profchall)

        if not game.exists():
            game = Game.objects.filter(profile1=profchall, profile2=prof)[0]
            if game.turn2 != 0:
                game.turn2 = game.turn2 - 1
                game.save()
        else:
            game = game[0]
            if game.turn1 != 0:
                game.turn1 = game.turn1 - 1
                game.save()

        questionTitle = objJson['question']
        tag = findTag(objJson['theme'], objJson['category'], objJson['tag'])
        question = Question.objects.create_question(game=game, question=questionTitle, prof_ask=prof, tag=tag)

        return HttpResponse(content=question, status=200)
    else:
        return HttpResponse(content="Not a good request", status=400)