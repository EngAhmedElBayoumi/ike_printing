from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html', {})


def error_404_view(request, exception):
    pass

def privacy(request):
    return render(request, 'privacy.html', {})