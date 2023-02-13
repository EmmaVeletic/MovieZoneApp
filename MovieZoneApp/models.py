from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    platform = models.ForeignKey('StreamPlatform', on_delete=models.CASCADE, null=True,
                                 blank=True, related_name='movie_list')
    cover = models.ImageField(upload_to='poster/', blank=True)
    is_published = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def number_of_ratings(self):
        reviews = Review.objects.filter(movie=self)
        return len(reviews)

    def avg_ratings(self):
        sum = 0
        reviews = Review.objects.filter(movie=self)
        for review in reviews:
            sum += review.rating

        if len(reviews) > 0:
            return sum / len(reviews)
        else:
            return 0


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField(max_length=360, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)

    def __str__(self):
        return "Rating for movie " + str(self.movie.title)

