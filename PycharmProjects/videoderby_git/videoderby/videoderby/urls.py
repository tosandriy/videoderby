from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
import notifications.urls
from . import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.blank_view),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('main/', views.main_view, name='first_index_page'),
    path('main/<page>/', views.main_view, name='index'),
    path('admin/', admin.site.urls),
    path('movie/<movie_pk>/', views.film_view, name='film'),
    path('movie/<movie_pk>/<comment_pk>/<action>/', views.CommentLikeView.as_view(), name='like_comment'),
    path('api/movie/<comment_pk>/<action>/', views.CommentLikeAPIToggle.as_view(), name='like_comment_api'),
    path('api/comment/<header>/<comment>/', views.CommentCreateAPI.as_view(), name='comment_api'),
    path('api/is_comment_unique/<comment>/<movie_pk>',views.IsCommentUniqueAPI.as_view(), name='unique_comment_api'),
    path('api/wishlist/<movie_pk>/', views.MovieWishListAPI.as_view(), name='wish_list_api'),
    path('api/watchlater/<movie_pk>/', views.MovieWatchLaterAPI.as_view(), name='watch_later_api'),
    path('api/clear_notifications/',views.ClearNotificationsAPI.as_view(),name='clear_notifications_api'),
    path('api/delete_wish_list_movie/<movie_pk>',views.WishListRemoveMovieAPI.as_view(),name="wish_list_remove_api"),
    path('login/', views.MyLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('films/', views.films_view,name='films'),
    path('profile/', views.profile_view,name='profile'),
    path('profile/watch_later/', views.watch_later_view,name='watch_later'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
