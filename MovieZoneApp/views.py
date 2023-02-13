from django.contrib.auth.models import User
from .models import Movie, Review, StreamPlatform
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (MovieSerializer, UserSerializer, ReviewSerializer,
                          StreamPlatformSerializer)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import mixins, generics

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,) #znaci da moze minjat i film


    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):

        if 'rating' in request.data:

            movie = Movie.objects.get(id=pk)
            rating = request.data['rating']
            user = request.user #user iz tokena koji je povezan sa userom
            #user = User.objects.get(id=1)

            try:
                review = Review.objects.get(user=user.id, movie=movie.id)
                review.rating = rating
                review.save()
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Review updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                review = Review.objects.create(user=user, movie=movie, rating=rating)
                serializer = ReviewSerializer(review, many=False)
                response = {'message': 'Review created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'you need to provide review'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def give_review(self, request, pk=None):

            if 'rating' in request.data and 'description' in request.data:

                movie = Movie.objects.get(id=pk)
                rating = request.data['rating']
                description = request.data['description']
                user = request.user  # user iz tokena koji je povezan sa userom
                # user = User.objects.get(id=1)

                try:
                    review = Review.objects.get(user=user.id, movie=movie.id)
                    review.rating = rating
                    review.description = description
                    review.save()
                    serializer = ReviewSerializer(review, many=False)
                    response = {'message': 'Review updated', 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    review = Review.objects.create(user=user, movie=movie, rating=rating, description=description)
                    serializer = ReviewSerializer(review, many=False)
                    response = {'message': 'Review created', 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)

            else:
                response = {'message': 'you need to provide review'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'you cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'you cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

'''class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def preform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)

        serializer.save(movie)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer'''


'''class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)'''

'''class StreamPlatformAv(APIView):

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailsAv(APIView):

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''