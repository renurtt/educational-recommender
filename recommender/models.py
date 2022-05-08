from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    username = models.TextField(null=True)
    externalId = models.IntegerField(null=True)
    score = models.FloatField(null=True)

    def __str__(self):
        return self.username + ": " + str(self.score)

    def __init__(self, username="", external_id=0, score=0):
        self.username = username
        self.externalId = external_id
        self.score = score


class SimilarUserResponse(models.Model):
    similarUsers = []

    def __str__(self):
        return '1'
