
from django.contrib import admin
from django.urls import path, include
from accounts import urls
from banner_and_posters import urls
from call_expert import urls
from product import urls
from contact_us import urls
from home import urls
from pricing import urls
from dragon import urls
from senior_dragon import urls
from senior_unicorn import urls
from unicorn import urls
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
    path("dragon/",include("dragon.urls")),
    path("senior_dragon/",include("senior_dragon.urls")),
    path("senior_unicorn/",include("senior_unicorn.urls")),
    path("unicorn/",include("unicorn.urls")),
    path('paypal-ipn/', include('paypal.standard.ipn.urls')), 
        ]

#media , static url
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
]



handler404 = 'home.views.error_404_view'
#handler500 = 'home.views.error_404_view'






