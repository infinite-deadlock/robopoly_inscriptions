from django.db import models
from django.utils import timezone

class Membre(models.Model):
    sciper = models.IntegerField(default=0)
    first_name = models.CharField(max_length=200, default="Pas de prénoms")
    name = models.CharField(max_length=200, default="Pas de noms")
    mail = models.CharField(max_length=200, default="Pas de mail")
    title = models.CharField(max_length=10, default="Pas de titre")
    section = models.CharField(max_length=50, default="Pas de section")
    phone_number = models.CharField(max_length=20, default="Pas de numéro")
    inscription_date_robopoly = models.DateTimeField(default=timezone.now)
