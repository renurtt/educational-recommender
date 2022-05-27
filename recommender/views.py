from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .SimilaritiesLookUp import SimilaritiesLookUp
from .models import SimilarUserResponse, User, MatchingMaterialsResponse
from .serializers import SimilarUserResponseSerializer, UserSerializer, LearningMaterialSerializer, \
    MatchingMaterialsResponseSerializer


class SimilarUsersInSkillSet(APIView):
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

        other_users = [{'username': x.get('username'),
                        'external_id': x.get('externalId'),
                        'skill_set': x.get('skillSet'),
                        'desired_position': x.get('desiredPosition')} for x in
                       request.data.get('otherUsers')]

        threshold = request.data.get('threshold')
        if threshold is None:
            threshold = 0

        similar_user_response = SimilarUserResponse()

        similar_user_response.similarUsers = SimilaritiesLookUp.get_similarities_in_skill_set(target_user_sill_set,
                                                                                              other_users,
                                                                                              threshold)

        similar_user_response.similarUsers = [UserSerializer(x).data for x in similar_user_response.similarUsers]

        serializer = SimilarUserResponseSerializer(similar_user_response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarUsersInDesiredPosition(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        # similar_user_response.similar_users = ['123', request.data.get('user')]

        target_user_sill_set = request.data.get('targetUser').get('desiredPosition')

        other_users = [{'username': x.get('username'),
                        'external_id': x.get('externalId'),
                        'skill_set': x.get('skillSet'),
                        'desired_position': x.get('desiredPosition')} for x in
                       request.data.get('otherUsers')]

        threshold = request.data.get('threshold')
        if threshold is None:
            threshold = 0

        similar_user_response = SimilarUserResponse()

        similar_user_response.similarUsers = SimilaritiesLookUp.get_similarities_in_desired_position(
            target_user_sill_set, other_users,
            threshold)

        similar_user_response.similarUsers = [UserSerializer(x).data for x in similar_user_response.similarUsers]

        serializer = SimilarUserResponseSerializer(similar_user_response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarContent(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    similarUsersLookup = SimilaritiesLookUp()

    def post(self, request, *args, **kwargs):
        # similar_user_response.similar_users = ['123', request.data.get('user')]
        target_user_desc = request.data.get('targetUser').get('description')
        materials = [{'id': x.get('id'),
                      'overview': x.get('overview')}
                     for x in request.data.get('materials')]

        response = MatchingMaterialsResponse()
        response.matchingMaterials = self.similarUsersLookup.get_similar_materials(target_user_desc, materials)

        response.matchingMaterials = [LearningMaterialSerializer(x).data for x in response.matchingMaterials]
        print(response.matchingMaterials)
        serializer = MatchingMaterialsResponseSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)



