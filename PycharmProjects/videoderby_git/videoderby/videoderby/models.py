from django.db import models
from . import settings
from . import validators
from . import choices
from django.utils.timezone import now
from django.contrib.postgres import fields
from django.contrib.auth.models import User
from django.core.files import File
from urllib import request
from django.urls import reverse
from PIL import Image


class Director(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='videoderby/media/images/DirectorPhotos', default='no_photo.png')

    def __str__(self):
        return self.name


class Movie(models.Model):
    poster = models.ImageField(upload_to='videoderby/media/images/filmPosters', default='no_photo.png')
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True)
    movie_likes = models.ManyToManyField(to=User, related_name='wish_list')
    watch_later = models.ManyToManyField(to=User, related_name='watch_later')
    genre = fields.ArrayField(models.CharField(choices=choices.GENRE_CHOICES, max_length=20))
    description = models.TextField(default='')
    actors = fields.ArrayField(models.CharField(max_length=200))
    director = fields.ArrayField(models.CharField(max_length=200))
    duration = models.CharField(max_length=50)
    rating = models.FloatField(validators=[validators.validate_lte_10])
    country = fields.ArrayField(models.CharField(choices=choices.COUNTRIES, max_length=150))
    kp_id = models.IntegerField()
    series = models.BooleanField(default=True)
    release = models.DateField(default=now)
    compositor = fields.ArrayField(models.CharField(max_length=200), null=True)
    local_rating = models.FloatField(default=0)
    local_rating_count = models.FloatField(default=0)

    def append_rating(self,rate):
        self.local_rating = (self.local_rating_count * self.local_rating + rate) / (self.local_rating_count + 1)
        self.local_rating_count += 1
        self.save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("film", kwargs={"movie_pk": self.pk})


class MovieImage(models.Model):
    movie = models.ForeignKey(to=Movie,on_delete=models.CASCADE,related_name="gallery")
    image = models.ImageField(upload_to='videoderby/media/ActorPhotos', default='no_photo.png')


class Comment(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="comments")
    comment_header = models.CharField(max_length=100)
    comment = models.CharField(max_length=800)
    addressed_to = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name="comments")
    rate = models.IntegerField()
    published = models.DateTimeField(default=now)
    total_likes = models.ManyToManyField(to=User,related_name="likes_comment", blank=True)
    total_dislikes = models.ManyToManyField(to=User,related_name="dislikes_comment", blank=True)

    def __str__(self):
        return self.comment_header

    def get_api_like_url(self,):
        return reverse("like_comment_api",kwargs={"comment_pk": self.pk,"action": "like"})

    def get_api_dislike_url(self,):
        return reverse("like_comment_api",kwargs={"comment_pk": self.pk,"action": "dislike"})


class Teaser(models.Model):
    title = models.CharField(max_length=200)
    background = models.ImageField(upload_to='videoderby/media/images/TeaserPhotos', default='no_photo.png')
    movie = models.OneToOneField(to=Movie, related_name='teaser', on_delete=models.CASCADE)
    upload = models.DateField(default=now)

    def __str__(self):
        return self.title


class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_wish_list")
    movies = fields.ArrayField(models.CharField(max_length=80))


class Profile(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name="profile")
    picture = models.ImageField(upload_to="images/UserPictures",default="videoderby/media/images/no_photo.png")
    liked_comments = models.ManyToManyField(to=Comment,related_name="likes",blank=True)
    disliked_comments = models.ManyToManyField(to=Comment,related_name="dislikes",blank=True)
    liked_films = models.ManyToManyField(to=Movie,related_name="likes",blank=True)

    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)


class Notification(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_notifications')
    action = models.BooleanField()
    checked = models.BooleanField(default=False)
    comment = models.ForeignKey(to=Comment,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.to_user.username


def create_movie(poster, name, year, genre, description, actors,
                 director, duration, rating, country, kp_id, images, compositor, series=False, ):
    """
    Функция для автоматического добавления фильмов на сайт, я храню ее в моделях, т.к. я не знаю куда ее пихнуть,
    чтобы она работала и смотрелось красиво, так что оставил ее тут
    """
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
