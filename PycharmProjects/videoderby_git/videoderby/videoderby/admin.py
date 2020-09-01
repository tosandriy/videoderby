from django.contrib import admin
from .models import Movie, Director, Teaser, Comment, Profile, Notification

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Teaser)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Notification)