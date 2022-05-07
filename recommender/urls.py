from django.urls import include, path
from rest_framework import routers

from recommender.views import RecommenderApiView

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', RecommenderApiView.as_view()),
]
