from django.db import models
from . import settings
from . import validators
from . import choices
from django.utils.timezone import now
from django.contrib.postgres import fields
from django.contrib.auth.models import User


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


class Comments(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=800)


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
    director = models.ForeignKey(to=Director, related_name='movies', on_delete=models.CASCADE)
    duration = models.IntegerField()
    movie = models.FileField(upload_to="movies", default='no_photo.png')
    trailer = models.URLField()
    rating = models.FloatField(validators=[validators.validate_lte_10])
    country = fields.ArrayField(models.CharField(choices=choices.COUNTRYS, max_length=150))
    published = models.BooleanField()
    kp_id = models.IntegerField()
    series = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Teaser(models.Model):
    title = models.CharField(max_length=200)
    background = models.ImageField(upload_to='videoderby/media/images/TeaserPhotos', default='no_photo.png')
    movie = models.OneToOneField(to=Movie, related_name='teaser', on_delete=models.CASCADE)
    upload = models.DateField(default=now)


class News(models.Model):
    title = models.CharField(max_length=80)
    posted = models.TimeField(default=now)
    text = models.TextField()
    photo = models.ImageField(upload_to='videoderby/media/images/NewsPhotos', default='no_photo.png')


class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = fields.ArrayField(models.CharField(max_length=80))
