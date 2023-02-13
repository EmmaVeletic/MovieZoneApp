from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import (MovieViewSet, UserViewSet, ReviewViewSet,
                    StreamPlatformViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('movies', MovieViewSet, basename='movie')
router.register('reviews', ReviewViewSet, basename="review")
router.register('streams', StreamPlatformViewSet, basename="stream")


urlpatterns = [
    path('', include(router.urls)),
    #path('streams/', StreamPlatformAv.as_view(), name='stream-list'),
    #path('streams/<int:pk>/', StreamPlatformDetailsAv.as_view(), name='stream'),
   # path('streams/<int:pk>/review', ReviewList.as_view(), name='review-list'), #svi reviewsi za odredjeni film
    #path('streams/review/<int:pk>', ReviewDetails.as_view(), name='review'), #pojedinaci review

]

