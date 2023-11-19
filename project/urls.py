"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts import urls
from banner_and_posters import urls
from call_expert import urls
from product import urls
from contact_us import urls
from home import urls
from pricing import urls
from django.conf.urls import handler404, handler500
#import settings
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("home.urls")),
    path("home/",include("home.urls")),
    path("accounts/",include("accounts.urls")),
    path("banner_and_posters/",include("banner_and_posters.urls")),
    path("call_expert/",include("call_expert.urls")),
    path("product/",include("product.urls")),
    path("contact_us/",include("contact_us.urls")),
    path("pricing/",include("pricing.urls")),
        ]

#media , static url
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
]



handler404 = 'home.views.error_404_view'






