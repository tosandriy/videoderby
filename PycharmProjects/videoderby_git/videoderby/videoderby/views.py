from django.db.models import Q, F
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.utils.timezone import now
from django.utils import timezone
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .forms import UserUpdateForm, ProfileUpdateForm
from . import models
from . import choices
from . import forms


def main_view(request,page=1):
    notifications = None
    notifications2 = None
    if not request.user.is_anonymous :
        notifications = User.objects.all().filter(username=request.user.username
                                                  ).get().user_notifications.all().filter(checked=True)
        notifications2 = User.objects.all().filter(username=request.user.username
                                                   ).get().user_notifications.all().filter(checked=False)
    films = models.Movie.objects.all().order_by("name")
    new_films = models.Movie.objects.all().order_by("release")
    teasers = models.Teaser.objects.all().order_by("movie__rating")[:3]
    genres = choices.GENRE_CHOICES
    year_cur = now().year
    years = (year_cur-x for x in range(100))
    best_films = models.Movie.objects.all().order_by("-rating")[:20]

    p = Paginator(films,20)
    try:
        page = int(page)
        cur_page = p.page(page)
    except:
        cur_page = p.page(1)
    films = cur_page.object_list
    next_page_list = []
    prev_page_list = []
    last_page = None
    first_page = None
    if cur_page.has_previous():
        prev_page_list.append(p.page(page - 1))
        if prev_page_list[0].has_previous():
            prev_page_list.append(p.page(page - 2))
            if p.page(page - 2).has_previous():
                first_page = p.page(1)
    if cur_page.has_next():
        next_page_list.append(p.page(page + 1))
        if next_page_list[-1].has_next():
            next_page_list.append(p.page(page + 2))
            if next_page_list[-1].has_next():
                if p.page(page + 3).has_next() :
                    if p.page(page + 4).has_next():
                        last_page = p.get_page(-1)

    prev_page_list.reverse()

    if len(new_films) > 8:
        new_films = new_films[:8]

    if request.GET :
        try:
            search = request.GET["search"]
            return redirect(f'/films/?name={search}')
        except:
            pass
        try:
            genre = request.GET["genre"]
        except:
            genre = None
        try:
            video_type = request.GET["filter_choose"]
        except:
            video_type = None
        try:
            year = request.GET["year"]
        except:
            year = None
        if video_type == "films":
            video_type = False
        else:
            video_type = True
        queryset = models.Movie.objects.all().filter(series=video_type)
        if genre:
            queryset = queryset.filter(genre__contains=[genre,])
        if year:
            queryset = queryset.filter(year=year)
        films = list(queryset.order_by("-rating"))

    return render(request, "index.html", {"films" : films,
                                          "new_films" : new_films,
                                          "teasers" : teasers,
                                          "genres" : genres,
                                          "years" : years,
                                          "best_films" : best_films,
                                          "first_page" : first_page,
                                          "prev_page_list": prev_page_list,
                                          "cur_page": cur_page,
                                          "next_page_list": next_page_list,
                                          "last_page": last_page,
                                          "notifications": notifications,
                                          "notifications2": notifications2,
                                          })


def film_view(request,movie_pk):
    notifications = None
    notifications2 = None
    if not request.user.is_anonymous :
        notifications = User.objects.all().filter(username=request.user.username
                                                  ).get().user_notifications.all().filter(checked=True)
        notifications2 = User.objects.all().filter(username=request.user.username
                                                   ).get().user_notifications.all().filter(checked=False)
    teasers = models.Teaser.objects.all().order_by("movie__rating")
    movie = models.Movie.objects.all().filter(pk=movie_pk).get()
    main_actors = movie.actors[:3]

    if request.GET :
        try:
            search = request.GET["search"]
            return redirect(f'/films/?name={search}')
        except:
            pass

    if request.POST:
        rate = request.POST["score"]
        comment = request.POST["comment"]
        try:
            header = request.POST["comment_header"]
        except:
            header = ""
        if comment and rate:
            if not request.user.comments.all().filter(addressed_to=movie):
                movie.append_rating(int(rate))
                add_comment(request,user=request.user, comment_header=header, comment=comment, addressed_to=movie, rate=int(rate))
                return redirect("film",movie_pk=movie_pk)
    comments = movie.comments.all()
    return render(request, "film.html", {"teasers" : teasers,
                                         "movie" : movie,
                                         "comments" : comments,
                                         "main_actors" : main_actors,
                                         "notifications" : notifications,
                                         "notifications2": notifications2,
                                         })


@login_required()
def add_comment(request,user, comment_header, comment, addressed_to, rate):
    comment = models.Comment(user=user, comment_header=comment_header,
                             comment=comment, addressed_to=addressed_to, rate=rate,)
    comment.save()


def register_view(request, *args, **kwargs):
    if not request.user.is_anonymous:
        return redirect("index")
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            email_subject = 'Activate your account'

            email = EmailMessage(
                    email_subject,
                    'Hi ' + request.user.username + ', Please the link below to activate your account \n' + "*link*",
                    'noreply@semycolon.com',
                    [request.POST['email']],
            )
            form.save()
            return redirect("login")
    else:
        form = forms.UserRegisterForm()

    return render(request, 'register.html', {'form': form})


class CommentLikeView(RedirectView):
    """
    Серверная часть отвечающая за лайки/дизлайки на комментариях
    """
    def get_redirect_url(self, *args, **kwargs):
        action = self.kwargs.get("action")
        movie_pk = self.kwargs.get("movie_pk")
        comment_pk = self.kwargs.get("comment_pk")
        movie = get_object_or_404(models.Movie, pk=movie_pk)
        comment = get_object_or_404(models.Comment, pk=comment_pk)
        url_ = movie.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if action == "like":
                if user in comment.total_likes.all():
                    comment.total_likes.remove(user)
                else:
                    comment.total_likes.add(user)
                if user in comment.total_dislikes.all():
                    comment.total_dislikes.remove(user)
            elif action == "dislike":
                if user in comment.total_dislikes.all():
                    comment.total_dislikes.remove(user)
                else:
                    comment.total_dislikes.add(user)
                if user in comment.total_likes.all():
                    comment.total_likes.remove(user)
            elif action == "delete":
                if comment.user == user:
                    comment.delete()
        return url_


class CommentCreateAPI(APIView):
    """
    API для AJAX, возвращает информацию о комментарии
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs) :
        header = self.kwargs.get("header")
        comment = self.kwargs.get("comment")
        comment_object = get_object_or_404(models.Comment,comment=comment, comment_header=header)
        data = {
                    'date': timezone.localtime().strftime("%Y-%m-%d %H:%M"),
                    'comment_pk': comment_object.pk,
                    'datahref1': str(comment_object.get_api_like_url()),
                    'datahref2': str(comment_object.get_api_dislike_url()),
                    'picture': comment_object.user.profile.picture.url
                    }
        return Response(data)





class CommentLikeAPIToggle(APIView):
    """
    API для AJAX, овтечающего за лайки/дизлайки
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs):
        action = self.kwargs.get("action")
        movie_pk = self.kwargs.get("movie_pk")
        comment_pk = self.kwargs.get("comment_pk")
        comment = get_object_or_404(models.Comment, pk=comment_pk)
        user = self.request.user
        updated = False
        liked = False
        disliked = False
        if user.is_authenticated :
            updated = True
            if action == "like" :
                liked = True
                if user in comment.total_likes.all() :
                    comment.total_likes.remove(user)
                    notification = models.Notification.objects.all().filter(from_user=user, to_user=comment.user,
                                                                            action=True, comment=comment)
                    notification.delete()
                else :
                    comment.total_likes.add(user)
                    notification = models.Notification(from_user=user, to_user=comment.user, action=True, comment=comment)
                    notification.save()
                if user in comment.total_dislikes.all() :
                    comment.total_dislikes.remove(user)
                    notification = models.Notification.objects.all().filter(from_user=user, to_user=comment.user,
                                                                            action=False, comment=comment)
                    notification.delete()
            elif action == "dislike" :
                disliked = True
                if user in comment.total_dislikes.all() :
                    comment.total_dislikes.remove(user)
                    notification = models.Notification.objects.all().filter(from_user=user, to_user=comment.user,
                                                                            action=False, comment=comment)
                else :
                    comment.total_dislikes.add(user)
                    notification = models.Notification(from_user=user, to_user=comment.user, action=False, comment=comment)
                    notification.save()
                if user in comment.total_likes.all() :
                    comment.total_likes.remove(user)
                    notification = models.Notification.objects.all().filter(from_user=user, to_user=comment.user,
                                                                            action=True, comment=comment)
                    notification.delete()
            elif action == "delete" :
                if comment.user == user :
                    comment.delete()
        data = {
                "updated" : updated,
                "liked" : liked,
                "disliked": disliked,
                "comment_pk": comment_pk,
        }
        return Response(data)


class MovieWishListAPI(APIView):
    """
    API для AJAX, отвечающий за добавление фильма в список желаний
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs):
        movie_pk = self.kwargs.get("movie_pk")
        movie = models.Movie.objects.all().get(pk=movie_pk)
        user = request.user
        if user in movie.movie_likes.all():
            pressed = False
            movie.movie_likes.remove(user)
        else:
            pressed = True
            movie.movie_likes.add(user)
        data = {
            "pressed": pressed,
            "movie_pk": movie_pk,
            "movie_name": movie.name,
        }
        return Response(data)


class MovieWatchLaterAPI(APIView):
    """
    API для AJAX, отвечающий за добавление фильма в список желаний
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs):
        movie_pk = self.kwargs.get("movie_pk")
        movie = models.Movie.objects.all().get(pk=movie_pk)
        user = request.user
        if user in movie.watch_later.all():
            pressed = False
            movie.watch_later.remove(user)
        else:
            pressed = True
            movie.watch_later.add(user)
        data = {
            "pressed": pressed,
            "movie_pk": movie_pk,
            "movie_name": movie.name,
        }
        return Response(data)


class ClearNotificationsAPI(APIView):
    """
    API для AJAX, обнуляющий уведомления
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None, *args, **kwargs):
        for notification in request.user.user_notifications.all().filter(checked=False):
            notification.checked = True
            notification.save()
        return Response({})


class IsCommentUniqueAPI(APIView):
    """
    API для AJAX, Проверяющий Комментарий на уникальность
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None, *args, **kwargs) :
        user = request.user
        movie_pk = self.kwargs.get("movie_pk")
        movie = models.Movie.objects.get(pk=movie_pk)
        single_comment = False
        if not user.comments.all().filter(addressed_to=movie):
            single_comment = True
        return Response({"is_unique": single_comment})


class WishListRemoveMovieAPI(APIView):
    """
        API для AJAX, удаляющий фильм из списка "Смотреть позже"
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs) :
        movie_pk = kwargs.get("movie_pk")
        request.user.user_wish_list.remove()
        return Response({})

def blank_view(request):
    return redirect("first_index_page")


class MyLoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    form_class = forms.UserLogInForm


def search_by_query(query):
    query = query.lower()
    final_query = ""
    for x in query :
        final_query += choices.en_ru_keyboard[x]
    query_2 = final_query.split(" ")
    query_1 = query.split(" ")
    matches = models.Movie.objects.all()
    matches2 = matches
    if query_1 :
        for q in query_1 :
            matches = matches.filter(Q(name__icontains=q))
        for q in query_2 :
            matches2 = matches2.filter(Q(name__icontains=q))
        result = matches | matches2
        return result
    return None


def films_view(request):
    notifications = None
    notifications2 = None
    if not request.user.is_anonymous :
        notifications = User.objects.all().filter(username=request.user.username
                                                  ).get().user_notifications.all().filter(checked=True)
        notifications2 = User.objects.all().filter(username=request.user.username
                                                   ).get().user_notifications.all().filter(checked=False)
    genres = choices.GENRE_CHOICES
    year_cur = now().year
    countries = choices.COUNTRIES
    years = (year_cur - x for x in range(100))
    years2 = (year_cur - x for x in range(100))
    query_set = models.Movie.objects.all()
    if request.GET:
        try:
            search = request.GET["search"]
            return redirect('films',{"name": search})
        except:
            pass
        try:
            name = request.GET["name"]
        except:
            name = None
        try:
            year = request.GET["year"]
        except:
            year = None
        try:
            year_1 = request.GET["year_1"]
        except:
            year_1 = None
        try:
            year_2 = request.GET["year_2"]
        except:
            year_2 = None
        try:
            country = request.GET["country"]
        except:
            country = None
        try:
            genre = request.GET["genre"]
        except:
            genre = None

        if name:
            query_set = search_by_query(name)
        if year:
            query_set = query_set.filter(year=year)
        if year_1 or year_2:
            query_set = query_set.annotate(int_year=F('year'))
            if not year_2:
                query_set = query_set.filter(int_year__gte=int(year_1))
            elif not year_1:
                query_set = query_set.filter(int_year__lte=int(year_2))
            elif year_1 and year_2:
                query_set = query_set.filter(int_year__lte=int(year_2)).filter(int_year__gte=int(year_1))
        if country:
            query_set = query_set.filter(country__contains=(country,))
        if genre:
            query_set = query_set.filter(genre__contains=(genre,))
    return render(request, 'films.html', {"genres" : genres,
                                          "years" : years,
                                          "years2": years2,
                                          "countries": countries,
                                          "films": list(set(query_set.order_by('rating'))),
                                          "notifications" : notifications,
                                          "notifications2": notifications2,
                                          })


@login_required()
def profile_view(request):
    notifications = None
    notifications2 = None
    if not request.user.is_anonymous :
        notifications = User.objects.all().filter(username=request.user.username
                                                  ).get().user_notifications.all().filter(checked=True)
        notifications2 = User.objects.all().filter(username=request.user.username
                                                   ).get().user_notifications.all().filter(checked=False)
    user = request.user
    date_joined = user.date_joined.strftime("%Y-%m-%d")
    wish_list = user.wish_list.all()
    if request.GET:
        try:
            search = request.GET["search"]
            return redirect(f'/films/?name={search}')
        except:
            pass
    if request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            return redirect('profile')
    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    likes = user.likes_comment.all()
    dislikes = user.dislikes_comment.all()
    comments = user.comments.all()
    comment_pool = likes | dislikes | comments
    final_action_dict = {}
    for action in comment_pool.order_by("published"):
        if action in likes:
            final_action_dict[action] = f"поставил лайк на отзыв у "
        elif action in dislikes:
            final_action_dict[action] = f"поставил дизлайк на отзыв у "
        elif action in comments:
            final_action_dict[action] = f"оставил отзыв на"
    action_list = []
    if final_action_dict:
        for key in final_action_dict:
            action_list.append((key, final_action_dict[key]))
    return render(request,"user.html", {
                                        "wish_list": wish_list,
                                        "date_joined": date_joined,
                                        "comment_list": action_list,
                                        'u_form' : u_form,
                                        'p_form' : p_form,
                                        "notifications" : notifications,
                                        "notifications2": notifications2,
                                        })

@login_required()
def watch_later_view(request):
    notifications = None
    if request.user.is_authenticated:
        notifications = request.user.user_notifications.all()
    user = request.user
    watch_later_list = user.watch_later.all()
    return render(request,"watch_later.html",{"watch_later_list": watch_later_list,
                                              "notifications": notifications})

