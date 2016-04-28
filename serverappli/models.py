# -*- coding: utf-8 -*
import hashlib
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

"""
ICI SONT DEFINIES LES TABLES DE LA BASE DE DONNEES.
SOYEZ PRUDENTS
	- Les champs objects dans chaque table désignent leur Manager -> à utiliser pour créer
"""

""" -------------------------------------------------------------- Profile -------------------------------------------------------------- """
class ProfileManager(models.Manager):
	"""
	Manager de la table Profile
		- create_profile(user, description, pseudo [, avatar] [, pourcentage])
	"""
	def create_profile(self, user, description, pseudo, avatar=None, pourcentage=60):
		if avatar is None:
			avatar = "http://www.gravatar.com/avatar/" + hashlib.md5(user.email.encode("utf-8")).hexdigest() + ".jpg?d=identicon"
		profile, created = self.get_or_create(id_user=user, description=description, pseudo=pseudo, avatar=avatar, pourcentage=pourcentage)
		return profile

class Profile(models.Model):
	"""
	Contient les profils des utilisateurs :
		- id_user       est la clé secondaire vers User
		- description   est une string
		- pseudo        est une string unique
		- avatar        est une string unique
		- pourcentage   est un nombre compris entre 25 et 100, par défaut à 60
	"""
	id_user = models.ForeignKey(settings.AUTH_USER_MODEL)
	description = models.CharField(max_length=500)
	pseudo = models.CharField(max_length=50, default="", unique=True)
	avatar = models.CharField(max_length=100, default="http://www.gravatar.com/avatar/0.jpg?d=identicon", unique=True)
	pourcentage = models.PositiveSmallIntegerField(validators=[MinValueValidator(25), MaxValueValidator(100)], default=60)
	objects = ProfileManager()
	def __str__(self):
		return "Profile [" + str(self.id_user) + "] " + str(self.pseudo) + " - " + str(self.description) + " - " + str(self.pourcentage)

""" -------------------------------------------------------------- Theme --------------------------------------------------------------- """
class ThemeManager(models.Manager):
	"""
	Manager de la table Theme
		- create_theme(title)
	"""
	def create_theme(self, title):
		theme, created = self.get_or_create(theme=title)
		return theme

class Theme(models.Model):
	"""
	Contient les thèmes :
		- theme est une string unique
	"""
	theme = models.CharField(max_length=50, unique=True)
	objects = ThemeManager()
	def __str__(self):
		return self.theme

""" -------------------------------------------------------------- Category ------------------------------------------------------------ """
class CategoryManager(models.Manager):
	"""
	Manager de la table Category
		- create_category(title, theme)
	"""
	def create_category(self, title, theme):
		category, created = self.get_or_create(category=title, id_theme=theme)
		return category

class Category(models.Model):
	"""
	Contient les catégories :
		- id_theme est la clé secondaire vers Theme
		- category est une string
	"""
	id_theme = models.ForeignKey('Theme')
	category = models.CharField(max_length=100)
	objects = CategoryManager()
	def __str__(self):
		return str(self.id_theme) + "/" + self.category

""" -------------------------------------------------------------- Tag ----------------------------------------------------------------- """
class TagManager(models.Manager):
	"""
	Manager de la table Tag
		- create_tag(title, category)
	"""
	def create_tag(self, title, category):
		tag, created = self.get_or_create(tag=title, id_category=category)
		return tag

class Tag(models.Model):
	"""
	Contient les tags :
		- id_category est la clé secondaire vers Category
		- tag         est une string
	"""
	id_category = models.ForeignKey('Category')
	tag = models.CharField(max_length=200)
	objects = TagManager()
	def __str__(self):
		return str(self.id_category) + "/" + self.tag

""" -------------------------------------------------------------- ListTags ------------------------------------------------------------ """
class ListTagsManager(models.Manager):
	"""
	Manager de la table ListTags
		- create_listTags(profile, tag [, date])
	"""
	def create_listTags(self, profile, tag, date=datetime.now()):
		listtags, created = self.get_or_create(id_profile=profile, id_tag=tag, date=date)
		return listtags

class ListTags(models.Model):
	"""
	Contient les associations entre un tag et un profil :
		- id_profile est la clé secondaire vers Profile
		- id_tag  est la clé secondaire vers Tag
		- date    est une date valant par défaut le moment de l'insertion
	"""
	id_profile = models.ForeignKey('Profile')
	id_tag = models.ForeignKey('Tag')
	date = models.DateTimeField(auto_now_add=True)
	objects = ListTagsManager()
	def __str__(self):
		return "ListTags [" + str(self.id_profile) + "] " + str(self.id_tag)

""" -------------------------------------------------------------- Checkin ------------------------------------------------------------- """
class CheckinManager(models.Manager):
	"""
	Manager de la table Checkin
		- create_checkin(user, latitude, longitude [, date])
	"""
	def create_checkin(self, user, latitude, longitude, date=datetime.now()):
		checkin, created = self.get_or_create(id_user=user, latitude=latitude, longitude=longitude, date=date)
		return checkin

class Checkin(models.Model):
	"""
	Contient les checkins d'un utilisateur :
		- id_user   est la clé secondaire vers User
		- latitude  est un float
		- longitude  est un float
		- date      est une date valant par défaut le moment de l'insertion
	"""
	id_user = models.ForeignKey(settings.AUTH_USER_MODEL)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	objects = CheckinManager()
	def __str__(self):
		return "Checkin [" + str(self.id_user) + " (" + str(self.date) + ") : " + str(self.latitude) + ", " + str(self.longitude) + "]"

""" -------------------------------------------------------------- Game ---------------------------------------------------------------- """
class GameManager(models.Manager):
	"""
	Manager de la table Game
		- create_game(profile1, profile2 [, turn1] [, turn2] [, date])
	"""
	def create_game(self, profile1, profile2, turn1=60, turn2=60, startDate=None):
		prev = self.filter(profile1=profile2, profile2=profile1)
		if len(prev) == 0:
			game, created = self.get_or_create(profile1=profile1, profile2=profile2, turn1=turn1, turn2=turn2, startDate=startDate)
			return game
		return prev[0]

class Game(models.Model):
	"""
	Contient les parties entre deux utilisateurs :
		- profile1   est la clé secondaire vers Profile nommée game_creator
		- profile2   est la clé secondaire vers Profile nommée game_challenger
		- turn1      est un int représentant le nombre de questions que profile1 peut poser
		- turn2      est un int représentant le nombre de questions que profile2 peut poser
		- startDate  est une date valant par défaut le moment de l'insertion
	"""
	profile1 = models.ForeignKey("Profile", related_name="game_creator")
	profile2 = models.ForeignKey("Profile", related_name="game_challenger")
	turn1 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=3)
	turn2 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=3)
	startDate = models.DateTimeField(auto_now_add=False, null=True)
	objects = GameManager()
	def __str__(self):
		return "Game [" + str(self.startDate) + "] " + str(self.profile1.pseudo) + " + " + str(self.profile2.pseudo) + ", turn1=" + str(self.turn1) + ", turn2=" + str(self.turn2)

""" -------------------------------------------------------------- Question ------------------------------------------------------------ """
class QuestionManager(models.Manager):
	"""
	Manager de la table Question
		- create_question(game, prof_ask, question, tag [, askDate])
	"""
	def create_question(self, game, prof_ask, question, tag, askDate=0):
		if askDate == 0:
			askDate = datetime.now()
		question, created = self.get_or_create(id_game=game, question=question, prof_ask=prof_ask, id_tag=tag, askDate=askDate)
		return question

class Question(models.Model):
	"""
	Contient les questions posées par les utilisateurs dans les parties :
		- id_game   est la clé secondaire vers Game
		- prof_ask  est la clé secondaire vers Profile
		- id_tag    est la clé secondaire vers Tag
		- question  est une string représentant la question posée
		- askDate   est une date représentant la date à laquelle la question a été posée
	"""
	id_game = models.ForeignKey("Game")
	prof_ask = models.ForeignKey("Profile")
	id_tag = models.ForeignKey("Tag")
	question = models.CharField(max_length=100)
	askDate = models.DateTimeField()
	# ansDate = models.DateTimeField(auto_now_add=False, null=True, default=None)
	objects = QuestionManager()
	def __str__(self):
		return "Question [" + self.question + "] asked=" + self.askDate.strftime('%d/%m/%Y %H:%M:%S') #+ ", answered=" + str(self.ansDate)

""" -------------------------------------------------------------- Friendship ---------------------------------------------------------- """
class FriendshipManager(models.Manager):
	def create_friendship(self, profile1, profile2, date=datetime.now()):
		prev = self.filter(profile1=profile2, profile2=profile1)
		if len(prev) == 0:
			friendship, created = self.get_or_create(profile1=profile1, profile2=profile2, date=date)
			return friendship
		return prev[0]
class Friendship(models.Model):
	profile1 = models.ForeignKey("Profile", related_name="friendship_creator")
	profile2 = models.ForeignKey("Profile", related_name="friendship_other")
	date = models.DateTimeField(auto_now_add=True)
	objects = FriendshipManager()
	def __str__(self):
		return "Friendship [" + str(self.date) + "] " + str(self.profile1.pseudo) + " + " + str(self.profile2.pseudo)

""" -------------------------------------------------------------- CHAT ---------------------------------------------------------- """
class ChatManager(models.Manager):
	def create_chat(self, fromProfile, toProfile, messageSend, date=datetime.now()):
		chat, created = self.get_or_create(fromProfile=fromProfile, toProfile=toProfile, messageSend=messageSend, date=date)
		return chat
class Chat(models.Model):
	fromProfile = models.ForeignKey("Profile", related_name="message_creator")
	toProfile = models.ForeignKey("Profile", related_name="message_other")
	messageSend = models.TextField(default="")
	date = models.DateTimeField(auto_now_add=True)
	objects = ChatManager()
	def __str__(self):
		return "Message [" + str(self.date) + "] " + str(self.fromProfile.pseudo) + " to " + str(self.toProfile.pseudo) + " : " + str(self.messageSend)
