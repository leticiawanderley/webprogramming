from django.db import models

"""Model of Actor
"""   
class Actor(models.Model):
	name = models.CharField(max_length=50)
	nationality = models.CharField(max_length=50)

"""Model of Director
"""
class Director(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)

"""Model of Film
"""
class Film(models.Model):
	title = models.CharField(max_length=50)
	year = models.PositiveSmallIntegerField(blank=True, null=True)
	genre = models.CharField(max_length=16)
	director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
	actors = models.ManyToManyField(Actor, blank=True)

"""Model of Award
"""
class Award(models.Model):
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=50, null=True)
	film = models.ForeignKey(Film, on_delete=models.CASCADE)
