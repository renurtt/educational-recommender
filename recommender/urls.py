from django.urls import include, path
from rest_framework import routers

from recommender.views import SimilarUsersInSkillSet, SimilarUsersInDesiredPosition, SimilarContent

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('similarUsersInSkillSet', SimilarUsersInSkillSet.as_view()),
    path('similarUsersInDesiredPosition', SimilarUsersInDesiredPosition.as_view()),
    path('similarContentForUser', SimilarContent.as_view()),
]
