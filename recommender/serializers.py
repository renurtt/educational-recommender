from rest_framework import serializers

from recommender.models import SimilarUserResponse


class SimilarUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarUserResponse
        fields = ["similar_users"]
