# -*- coding: utf-8 -*
from django.core.management.base import BaseCommand, CommandError
from serverappli.models import Game

class Command(BaseCommand):
    help = 'Reset le nombre de questions pour chaque joueur quand il en a moins de 3'

    def handle(self, *args, **options):
        allGames = Game.objects.all()
        for g in allGames:
            if (g.turn1 < 60):
                g.turn1 = 60
            if (g.turn2 < 60):
                g.turn2 = 60
            g.save();