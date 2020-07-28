from django.contrib import admin
from .models import Actor, Movie, Director, Images, Teaser, News

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Images)
admin.site.register(Teaser)
admin.site.register(News)
