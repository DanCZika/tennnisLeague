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
    active = models.BooleanField()
    wins = models.IntegerField(default=0)
    runnerups = models.IntegerField(default=0) 

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.user)

class Round(models.Model):
    """docstring for ."""
    name = models.CharField(max_length=50)
    active = models.BooleanField()
    description = models.CharField(max_length=252)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    winner = models.CharField(max_length=255)
    runnerup = models.CharField(max_length=255)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Entry(models.Model):
    """docstring for ."""
    player  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default = 0)
    matches_played = models.IntegerField(default = 0)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.player

class Match(models.Model):
    """docstring for ."""
    player1  = models.CharField(max_length=255)
    player2  = models.CharField(max_length=255)
    point1 = models.IntegerField()
    point1 = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    court = models.CharField(max_length=255)
    played = models.BooleanField()
    score = models.CharField(max_length=20)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(str(player1) + " - " +str(player2))

class MatchEntry(models.Model):
    """docstring for ."""
    player = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(match)