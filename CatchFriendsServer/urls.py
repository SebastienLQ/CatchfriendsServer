# -*- coding: utf-8 -*
from django.conf.urls import patterns, include, url, handler404
from django.contrib import admin

from serverappli.views import simpleGet, dispatchDataBase, getAllThemes, getCategories, getAllTags, getTagsLetter, dispachAddTags, test, test2, gravatar
from serverappli.tagFunctions import getCurrentTags, getAskableCurrentTags
from serverappli.checkinFunctions import createCheckin, getHistoriqueCheckin
from serverappli.userFunctions import logUser, createUser, createProfile, getProfile, updateProfile, getMyFriends, addFriend
from serverappli.challengeFunctions import getPossibleChallengers, getDemandesChallenges, getCurrentGames, getGameQuestions, addQuestion
from serverappli.bddFunctions import nettoyage, itunesDB, giantBombDB
from serverappli.errorHandlers import error404
from serverappli.chatFunctions import sendMessage, getMessage

"""
-------------------------------------- URLS DE TAGS ---------------------------------------------------------------------------------
cf/getCurrentTags$                                          ->  tagFunctions.getCurrentTags                 ->  Récupérer les tags d'un utilisateur
cf/getAskableCurrentTags$                                   ->  tagFunctions.getAskableCurrentTags          ->  Récupérer les tags qu'un utilisateur peut demander
cf/getAllThemes$                                            ->  views.getAllThemes                          ->  Récupérer tous les thèmes
cf/getCategories/(?P<theme>.{1,50})$                        ->  views.getCategories                         ->  Récupérer les catégories d'un thème
cf/getTags/(?P<theme>.{1,50})/(?P<category>.{1,50})$        ->  views.getAllTags                            ->  Récupérer les tags d'une catégorie
cf/getTags/(?P<theme>.{1,50})/(?P<category>.{1,50})/letter$ ->  views.getTagsLetter                         ->  Récupérer les tags d'une catégorie en fonction d'une recherche
cf/addTags$                                                 ->  views.dispachAddTags                        ->  Ajouter un tag au profil d'un utilisateur
-------------------------------------- URLS DE USER ET PROFIL -----------------------------------------------------------------------
cf/createUser$                                              ->  userFunctions.createUser                    ->  Créer un utilisateur
cf/createProfile$                                           ->  userFunctions.createProfile                 ->  Créer un profil pour un utilisateur
cf/logUser$                                                 ->  userFunctions.logUser                       ->  Connecter un utilisateur
cf/getProfile$                                              ->  userFunctions.getProfile                    ->  Récupérer le profil d'un utilisateur
cf/updateProfile$                                           ->  userFunctions.updateProfile                 ->  Mettre le profil d'un utilisateur à jour
cf/getFriends$                                              ->  userFunctions.getMyFriends                  ->  Récupérer les amis
cf/addFriend                                                ->  userFunctions.addFriend                     ->  Ajouter un ami
-------------------------------------- URLS DE CHECKIN ------------------------------------------------------------------------------
cf/checkin$                                                 ->  checkinFunctions.createCheckin              ->  Créer un checkin pour un utilisateur
cf/checkin/historique/(?P<user>\w{1,50})$                   ->  checkinFunctions.getHistoriqueCheckin       ->  Récupérer l'historique des checkins d'un utilisateur
-------------------------------------- URLS DE CHALLENGE ----------------------------------------------------------------------------
cf/possibleChallengers$                                     ->  challengeFunctions.getPossibleChallengers   ->  Récupérer les challengers possibles d'un utilisateur
cf/demandesChallenges$                                      ->  challengeFunctions.getDemandesChallenges    ->  Récupérer les demandes de challenge envers un utilisateur
cf/currentGames$                                            ->  challengeFunctions.getCurrentGames          ->  Récupérer les parties en cours d'un utilisateur
cf/gameQuestions$                                           ->  challengeFunctions.getGameQuestions         ->  Récupérer les questions d'une partie d'un utilisateur
cf/addQuestion$                                             ->  challengeFunctions.addQuestion              ->  Ajouter une question à une partie d'un utilisateur
-------------------------------------- URLS DE TEST ---------------------------------------------------------------------------------
cf/test$                                                    ->  views.test                                  ->  Fonction de Test
cf/test2$                                                   ->  views.test2                                 ->  Fonction de Test
-------------------------------------- URLS DE DB -----------------------------------------------------------------------------------
/!\    cf/nettoyage$                                         ->  bddFunctions.nettoyage                      ->  Vide et remplit à nouveau la base de données.    /!\
cf/makeItunesDB$                                            ->  bddFunctions.itunesDB                       ->  Récupère beaucoup de tags depuis itunes vers itunes_data.json
cf/makeGiantBombDB$                                         ->  bddFunctions.giantBombDB                    ->  Récupère beaucoup de tags depuis giantbomb vers giantbomb_data.json
"""
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^cf/getCurrentTags$', getCurrentTags),
    url(r'^cf/getAskableCurrentTags$', getAskableCurrentTags),
    url(r'^cf/getAllThemes$', getAllThemes),
    url(r'^cf/getCategories/(?P<theme>.{1,50})$', getCategories),
    url(r'^cf/getTags/(?P<theme>.{1,50})/(?P<category>.{1,50})$', getAllTags),
    url(r'^cf/getTags/(?P<theme>.{1,50})/(?P<category>.{1,50})/letter$', getTagsLetter),
    url(r'^cf/addRemoveTags$', dispachAddTags),

    url(r'^cf/createUser$', createUser),
    url(r'^cf/createProfile$', createProfile),
    url(r'^cf/logUser$', logUser),
    url(r'^cf/getProfile$', getProfile),
    url(r'^cf/updateProfile$', updateProfile),
    url(r'^cf/addFriend$', addFriend),

    url(r'^cf/checkin$', createCheckin),
    url(r'^cf/checkin/historique/(?P<user>\w{1,50})$', getHistoriqueCheckin),

    url(r'^cf/possibleChallengers$', getPossibleChallengers),
    url(r'^cf/demandesChallenges$', getDemandesChallenges),
    url(r'^cf/currentGames$', getCurrentGames),
    url(r'^cf/gameQuestions$', getGameQuestions),
    url(r'^cf/addQuestion$', addQuestion),

    url(r'^cf/test$', test),
    url(r'^cf/test2$', test2),
    url(r'^cf/gravatar$', gravatar),

    url(r'^cf/nettoyage$', nettoyage),
    url(r'^cf/makeItunesDB$', itunesDB),
    url(r'^cf/makeGiantBombDB$', giantBombDB),
    url(r'^cf/getFriends$', getMyFriends),
    url(r'^cf/getDataBase/(?P<username>\w{1,50})$', dispatchDataBase),
    # url(r'^cf/simple$', simpleGet),

    url(r'^cf/sendMessage$', sendMessage),
    url(r'^cf/getMessage$', getMessage)
)

handler404 = error404
