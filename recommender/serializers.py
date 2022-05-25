from rest_framework import serializers

from recommender.models import SimilarUserResponse, User, MatchingMaterialsResponse, LearningMaterial


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "externalId", "score"]


class SimilarUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarUserResponse
        fields = ["similarUsers"]
        serializers = UserSerializer


class LearningMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningMaterial
        fields = ["materialId", "score"]


class MatchingMaterialsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingMaterialsResponse
        fields = ["matchingMaterials"]
        serializers = LearningMaterialSerializer
