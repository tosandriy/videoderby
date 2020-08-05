from django.shortcuts import render,redirect
from . import models

from . import choices
from django.utils.timezone import now
from . import forms
from django.contrib.auth import views as auth_views


def main_view(request):
    films = models.Movie.objects.all().order_by("name")
    new_films = models.Movie.objects.all().order_by("release")
    teasers = models.Teaser.objects.all().order_by("movie__rating")
    genres = choices.GENRE_CHOICES
    year_cur = now().year
    years = (year_cur-x for x in range(100))
    best_films = models.Movie.objects.all().order_by("-rating")

    if len(new_films) > 8:
        new_films = new_films[:8]

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
        films = list(queryset.order_by("-rating"))

    return render(request, "index.html", {"films" : films,
                                          "new_films" : new_films,
                                          "teasers" : teasers,
                                          "genres" : genres,
                                          "years" : years,
                                          "best_films" : best_films,
                                          })


def film_view(request,movie_pk):
    teasers = models.Teaser.objects.all().order_by("movie__rating")
    movie = models.Movie.objects.all().filter(pk=movie_pk).get()

    return render(request, "film.html", {"teasers" : teasers,
                                         "movie" : movie,
                                         })


def register_view(request):
    print(request.user)
    if not request.user.is_anonymous:
        return redirect("index")
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = forms.UserRegisterForm()

    return render(request, 'register.html', {'form': form})


class MyLoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    form_class = forms.UserLogInForm
