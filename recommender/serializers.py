from rest_framework import serializers

from recommender.models import SimilarUserResponse, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "externalId", "score"]


class SimilarUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarUserResponse
        fields = ["similarUsers"]
        serializers = UserSerializer
