from django.shortcuts import render, redirect, reverse
from . import models
from . import kp_parser
from . import choices
from django.utils.timezone import now


def main_view(request):
    films = models.Movie.objects.all().order_by("name")
    new_films = models.Movie.objects.all().order_by("release")
    teasers = models.Teaser.objects.all().order_by("movie__rating")
    news = models.News.objects.all().order_by("posted")
    genres = choices.GENRE_CHOICES
    year_cur = now().year
    years = (year_cur-x for x in range(100))
    best_films = models.Movie.objects.all().order_by("-rating")
    if len(new_films) > 8:
        new_films = new_films[:8]

    if len(news) > 4:
        news = news[:4]
    if request.GET:
        genre = request.GET["genre"]
        video_type = request.GET["type"]
        year = request.GET["year"]
        if video_type == "films":
            video_type = False
        else:
            video_type = True
        queryset = models.Movie.objects.all().filter(series=video_type)
        if genre:
            queryset = queryset.filter(genre__contains=[genre,])
        if year:
            queryset = queryset.filter(release__year=year)
        films = list(queryset)

    return render(request, "index.html", {"films" : films,
                                          "new_films" : new_films,
                                          "news" : news,
                                          "teasers" : teasers,
                                          "genres" : genres,
                                          "years" : years,
                                          "best_films" : best_films,
                                          })


def actor_view(request,actor_pk):
    actor = models.Actor.objects.get(pk=actor_pk)
    roles = []
    avg_rating = 0
    photos = actor.photogallery.filter(actor=actor)
    films = actor.roles.all().order_by("rating")
    all_films = actor.roles.all().order_by("release")
    kp_table = actor.kp_table
    career, height, birth_day, place_of_birth, movie_count = kp_parser.actor_parser(kp_table)
    for film in films:
        roles += film.genre
        avg_rating+=film.rating
    roles = list(set(roles))
    avg_rating = round(avg_rating / len(films),1)
    lastrole = roles[-1]
    if len(roles) > 1:
        roles = roles[:-1]
    return render(request, "actor.html", {"actor" : actor,
                                          "genres" : roles,
                                          "last_genre" : lastrole,
                                          "career" : career,
                                          "height" : height,
                                          "birth_day" : birth_day,
                                          "place_of_birth" : place_of_birth,
                                          "movie_count" : movie_count,
                                          "avg_rating" : avg_rating,
                                          "films" : films,
                                          "photos" : photos,
                                          "all_films" : all_films,
                                          })
