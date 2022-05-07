from django.contrib.postgres.fields import ArrayField
from django.db import models


class SimilarUserResponse(models.Model):
    similar_users = ArrayField(models.TextField(null=True))

    def __str__(self):
        return '1'
