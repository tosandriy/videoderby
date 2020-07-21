from django.db import models
from . import validators
from . import choices
from django.utils.timezone import now
from django.contrib.postgres import fields


class Actor(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='videoderby/media/ActorPhotos', default='no_photo.png')

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='videoderby/media/images/DirectorPhotos', default='no_photo.png')

    def __str__(self):
        return self.name


class Movie(models.Model):
    poster = models.ImageField(upload_to='videoderby/media/images/filmPosters', default='no_photo.png')
    name = models.CharField(max_length=60)
    release = models.DateField(default=now)
    genre = fields.ArrayField(models.CharField(choices=choices.GENRE_CHOICES, max_length=20))
    description = models.TextField(default='')
    actors = models.ManyToManyField(to=Actor, related_name='roles')
    director = models.ManyToManyField(to=Director, related_name='movies')
    duration = models.IntegerField()
    movie = models.FileField(upload_to="movies", default='no_photo.png')
    trailer = models.URLField()
    rating = models.FloatField(validators=[validators.validate_lte_10])
    country = fields.ArrayField(models.CharField(choices=choices.COUNTRYS, max_length=150))

    def __str__(self):
        return self.name


