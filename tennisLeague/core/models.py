from email.policy import default
from nis import match
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class PlayerData(models.Model):
    """docstring for ."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    phone_number = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    win_count = models.IntegerField(default=0, null=True, blank=True)
    lose_count = models.IntegerField(default=0, null=True, blank=True)
    wins = models.IntegerField(default=0)
    runnerups = models.IntegerField(default=0)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.user)

class Round(models.Model):
    """docstring for ."""
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    description = models.CharField(max_length=252)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    winner = models.CharField(max_length=255,null=True, blank=True)
    runnerup = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Entry(models.Model):
    """docstring for ."""
    player  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default = 0)
    matches_played = models.IntegerField(default = 0)
    matches_won = models.IntegerField(default = 0)
    matches_lost = models.IntegerField(default = 0)
    bonus = models.IntegerField(default = 0)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.player.first_name) + ' ' + str(self.player.last_name)

class Match(models.Model):
    """docstring for ."""
    player1  = models.CharField(max_length=255)
    player2  = models.CharField(max_length=255)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    court = models.CharField(max_length=255,null=True, blank=True)
    played = models.BooleanField(default = False)
    score = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(str(self.player1) + " - " +str(self.player2))

class MatchEntry(models.Model):
    """docstring for ."""
    player = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return  str(self.player) + "---" + str(self.match)