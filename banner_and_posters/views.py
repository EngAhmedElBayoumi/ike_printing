from django.shortcuts import render

# Create your views here.

def banner_and_posters(request):
    return render(request, 'PosterAndBanners.html', {})