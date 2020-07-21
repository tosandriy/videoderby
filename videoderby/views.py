from django.shortcuts import render, redirect, reverse
from . import models
def main_view(request):
    films = models.Movie.objects.all()
    return render(request, "index.html", {"films" : films})
