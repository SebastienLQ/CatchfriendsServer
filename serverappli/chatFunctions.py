# -*- coding: utf-8 -*
import json
import logging
import hashlib
from django.db.models import Q
import collections

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from serverappli.models import Profile, Friendship, Chat
from serverappli.utils import myDumpJson

"""
Ces fonctions concernent les chats
On peut enregistrer les messages en bdd et les get
"""
@csrf_exempt
def sendMessage(request):
	if request.method == 'POST':
		objJson = json.loads(request.body.decode('utf-8'))
		message = objJson['message']
		fromProfile = Profile.objects.get(pseudo=objJson['from'])
		toProfile = Profile.objects.get(pseudo=objJson['to'])
		print("===DEBUT MESSAGE===")
		print("FROM : ",fromProfile.pseudo)
		print("TO : ",toProfile.pseudo)
		print("MESSAGE : ",objJson['message'])
		print("===FIN MESSAGE===")

		m = Chat.objects.create_chat(fromProfile=fromProfile, toProfile=toProfile, messageSend=message)
		return HttpResponse(status=200)
	else:
		return HttpResponse(content="Not a POST request", status=400)

@csrf_exempt
def getMessage(request):
	if request.method == 'POST':
		objJson = json.loads(request.body.decode('utf-8'))
		fromProfile = Profile.objects.get(pseudo=objJson['from'])
		toProfile = Profile.objects.get(pseudo=objJson['to'])
		# print("from pseudo", fromProfile.pseudo)
		# print("to pseudo", toProfile.pseudo)
		messages = Chat.objects.filter(Q(fromProfile=fromProfile) | Q(fromProfile=toProfile) | Q(toProfile=toProfile) | Q(toProfile=fromProfile)).order_by('date')
		# print("msg", messages)

		# for message in messages:
		#     print(message)
		#     print(type(message))

		res = []

		for message in messages:
		    # print("MSG de ",message.fromProfile, " " message.messageSend," !")
			# print("MSG de {0} à {1} : {2}".format(message.fromProfile.pseudo, message.toProfile.pseudo, message.messageSend));
			d = collections.OrderedDict()
			d['messageSend'] = message.messageSend
			d['fromProfile'] = message.fromProfile.pseudo
			d['toProfile'] = message.toProfile.pseudo
			res.append(d)

		return HttpResponse(json.dumps(res), content_type='application/json')
	else:
		return HttpResponse(content="Not a POST request", status=400)
