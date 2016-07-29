from django.conf.urls import url
from django.contrib import admin
from url_shortener import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^s/(\w+)', views.redirect_from_code),
]
