# -*- coding: utf-8 -*-

from serverappli.utils import themesStyle

class CurrentGamesDTO:
    def __init__(self, profile, turn):
        self.pseudo = profile.pseudo
        self.avatar = profile.avatar
        self.description = profile.description
        self.turn = turn

    def toJson(self):
        res = {}
        res["pseudo"] = self.pseudo
        res["avatar"] = self.avatar
        res["description"] = self.description
        res["turn"] = self.turn
        return res


class HistoriqueCheckinDTO:
    def __init__(self, checkin):
        self.latitude = checkin.latitude
        self.longitude = checkin.longitude

    def toJson(self):
        res = {}
        res["latitude"] = self.latitude
        res["longitude"] = self.longitude
        return res


class ProfileDTO:
    def __init__(self, profile, compatibility):
        self.pseudo = profile.pseudo
        self.avatar = profile.avatar
        self.description = profile.description
        self.compatibility = compatibility

    def toJson(self):
        res = {}
        res["pseudo"] = self.pseudo
        res["avatar"] = self.avatar
        res["description"] = self.description
        res["pourcentage"] = self.compatibility
        return res


class CategoryDTO:
    def __init__(self, category):
        self.category = category.category
        self.theme = category.id_theme.theme
        self.color = themesStyle[self.theme]['Color']
        self.icon = themesStyle[self.theme]['Icon']

    def toJson(self):
        res = {}
        res["category"] = self.category
        res["theme"] = self.theme
        res["color"] = "button-" + self.color
        res["icon"] = self.icon
        return res


class QuestionDTO:
    def __init__(self, question, answered, yourself):
        self.question = question.question
        self.tag = question.id_tag.tag
        self.category = question.id_tag.id_category.category
        self.theme = question.id_tag.id_category.id_theme.theme
        self.profile = question.prof_ask.pseudo
        self.profileAvatar = question.prof_ask.avatar
        self.date = question.askDate.strftime('%Y-%m-%dT%H:%M:%S')
        self.answer = answered
        self.answerText = "Oui" if self.answer else "Non"
        self.yourself = yourself
        self.color = themesStyle[self.theme]['Color']
        
    def toJson(self):
        res = {}
        res["question"] = self.question
        res["tag"] = self.tag
        res["category"] = self.category
        res["theme"] = self.theme
        res["profile"] = self.profile
        res["profileAvatar"] = self.profileAvatar
        res["date"] = self.date
        res["answer"] = self.answer
        res["answerText"] = self.answerText
        res["yourself"] = self.yourself
        res["color"] = self.color
        return res


class ValidCheckinsDTO:
    def __init__(self, profile, checkin, compatibility):
        self.pseudo = profile.pseudo
        self.avatar = profile.avatar
        self.description = profile.description
        self.compatibility = compatibility
        self.latitude = checkin.latitude
        self.longitude = checkin.longitude
        self.date = checkin.date.strftime('%d/%m/%Y')

    def toJson(self):
        res = {}
        res["pseudo"] = self.pseudo
        res["avatar"] = self.avatar
        res["description"] = self.description
        res["pourcentage"] = self.compatibility
        res["latitude"] = self.latitude
        res["longitude"] = self.longitude
        res["date"] = self.date
        return res