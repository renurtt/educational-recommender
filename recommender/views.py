from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .SimilaritiesLookUp import SimilaritiesLookUp
from .models import SimilarUserResponse, User
from .serializers import SimilarUserResponseSerializer, UserSerializer


class RecommenderApiView(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    """
        REST Endpoint, finds similar users on target user's skillSet and other users' skillSets
        Example:
            request:
            {
                "threshold": 0.3,
                "otherUsers": [
                    {
                        "username": "2",
                        "skillSet": "python:beginer"
                    },
                    {
                        "username": "3",
                        "skillSet": "python:proficient c#:beginer"
                    }
                ],
                "targetUser": {
                    "username": "123",
                    "skillSet": "python:proficient"
                }
            }
            response:
            {
                "similar_users": [
                    {
                        "username": "3",
                        "score": 0.7847555613034414
                    },
                    {
                        "username": "2",
                        "score": 0.37620501479919144
                    }
                ]
            }
    """

    def post(self, request, *args, **kwargs):
        # similar_user_response.similar_users = ['123', request.data.get('user')]

        target_user_sill_set = request.data.get('targetUser').get('skillSet')

        other_users = [{'username': x.get('username'), 'external_id': x.get('externalId'), 'skill_set': x.get('skillSet')} for x in
                       request.data.get('otherUsers')]

        threshold = request.data.get('threshold')
        if threshold is None:
            threshold = 0

        similar_user_response = SimilarUserResponse()

        similar_user_response.similarUsers = SimilaritiesLookUp.get_similarities(target_user_sill_set, other_users,
                                                                                  threshold)

        similar_user_response.similarUsers = [UserSerializer(x).data for x in similar_user_response.similarUsers]

        serializer = SimilarUserResponseSerializer(similar_user_response)
        return Response(serializer.data, status=status.HTTP_200_OK)
