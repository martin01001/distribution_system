from django.urls import path
from dist_sys import views
from django.conf.urls.static import static
from distrbution_system import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("form/", views.form, name="form"),
    path("api/get_result/", views.get_result, name="get_result"),
] + static(settings.STATIC_URL, documnet_root=settings.STATICFILES_DIRS)
