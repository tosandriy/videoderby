from django.db import models
from . import settings
from . import validators
from . import choices
from django.utils.timezone import now
from django.contrib.postgres import fields
from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import os
from urllib import request


class Actor(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='videoderby/media/ActorPhotos', default='no_photo.png')
    facts = fields.ArrayField(models.CharField(max_length=90))
    kp_table = models.TextField()

    def __str__(self):
        return self.name


class Images(models.Model):
    actor = models.ForeignKey(to=Actor, on_delete=models.CASCADE, related_name='photogallery')
    image = models.ImageField(upload_to='videoderby/media/ActorPhotos', default='no_photo.png')

    def __str__(self):
        return self.actor.name


class Director(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='videoderby/media/images/DirectorPhotos', default='no_photo.png')

    def __str__(self):
        return self.name


class Movie(models.Model):
    poster = models.ImageField(upload_to='videoderby/media/images/filmPosters', default='no_photo.png')
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    genre = fields.ArrayField(models.CharField(choices=choices.GENRE_CHOICES, max_length=20))
    description = models.TextField(default='')
    actors = fields.ArrayField(models.CharField(max_length=200))
    director = fields.ArrayField(models.CharField(max_length=200))
    duration = models.CharField(max_length=50)
    rating = models.FloatField(validators=[validators.validate_lte_10])
    country = fields.ArrayField(models.CharField(choices=choices.COUNTRYS, max_length=150))
    kp_id = models.IntegerField()
    series = models.BooleanField(default=True)
    release = models.DateField(default=now)
    compositor = fields.ArrayField(models.CharField(max_length=200))


    def __str__(self):
        return self.name


class MovieImage(models.Model):
    movie = models.ForeignKey(to=Movie,on_delete=models.CASCADE,related_name="gallery")
    image = models.ImageField(upload_to='videoderby/media/ActorPhotos', default='no_photo.png')


class Comment(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    comment_header = models.CharField(max_length=100)
    comment = models.CharField(max_length=800)
    addressed_to = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name="comments")
    rate = models.FloatField()
    published = models.TimeField(auto_now=True)
    total_likes = models.IntegerField()
    total_dislikes = models.IntegerField()


class SlaveComment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=800)
    addressed_to = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name="comments")
    published = models.TimeField(auto_now=True)
    total_likes = models.IntegerField()
    total_dislikes = models.IntegerField()


class Teaser(models.Model):
    title = models.CharField(max_length=200)
    background = models.ImageField(upload_to='videoderby/media/images/TeaserPhotos', default='no_photo.png')
    movie = models.OneToOneField(to=Movie, related_name='teaser', on_delete=models.CASCADE)
    upload = models.DateField(default=now)


class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = fields.ArrayField(models.CharField(max_length=80))


def create_movie(poster, name, year, genre, description, actors,
                 director, duration, rating, country, kp_id, images, compositor, series=False, ):
    """Функция для автоматического добавления фильмов на сайт, я храню ее в моделях, т.к. я не знаю куда ее пихнуть,
     чтобы она работала и смотрелось красиво, так что оставил ее тут"""
    movie = Movie(name=name, year=year, genre=list(genre), description=description, actors=list(actors),
                  director=list(director), duration=int(duration), rating=rating, country=list(country),
                  kp_id=kp_id, series=bool(series), compositor=list(compositor))
    poster_url = poster

    result = request.urlretrieve(poster_url)
    movie.poster.save("%s's poster" % movie.name, File(open(result[0], 'rb')))
    movie.save()

    num_list = [1,2,3,4,5,6,7,8]
    for image in list(images):
        print(image)
        movie_image = MovieImage(movie=movie)
        result = request.urlretrieve(image)
        movie_image.image.save("%s_image_%s" % (movie.name, num_list.pop()), File(open(result[0], 'rb')))
        movie_image.save()
