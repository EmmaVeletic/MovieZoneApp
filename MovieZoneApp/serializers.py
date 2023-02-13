from rest_framework import serializers
from .models import Movie, Review, StreamPlatform
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):

    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'username', 'password', 'days_since_joined')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'movie', 'user', 'rating',
                  'description', 'active', 'created', 'update')

class MovieSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'cover', 'platform',
                  'is_published', 'created', 'number_of_ratings', 'avg_ratings')

        def validate(self, data):
            if data.name['title'] == data.name['description']:
                raise serializers.ValidationError("Title and description should be different")
            else:
                return data

class StreamPlatformSerializer(serializers.ModelSerializer):
    movie_list = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'







