from django.conf.urls import url
from django.contrib import admin
from url_shortener import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/redirect_code/(.+)/', views.api_get_redirect_code),
    url(r'^api/redirect_code', views.api_create_redirect_code),
    url(r'^(.+)/', views.redirect_from_code),
]
