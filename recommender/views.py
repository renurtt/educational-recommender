from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .SimilaritiesLookUp import SimilaritiesLookUp
from .models import SimilarUserResponse
from .serializers import SimilarUserResponseSerializer


class RecommenderApiView(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request, *args, **kwargs):
        similar_user_response = SimilarUserResponse()

        # similar_user_response.similar_users = ['123', request.data.get('user')]
        similar_user_response.similar_users = SimilaritiesLookUp.get_similarities()

        serializer = SimilarUserResponseSerializer(similar_user_response)
        return Response(serializer.data, status=status.HTTP_200_OK)


