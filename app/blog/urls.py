from django.urls import path
from .views import Index, PostDetail, YandexTurbo, ParceObjects
from .custom_sitemap import custom_sitemap

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('post/<slug:slug>', PostDetail.as_view(), name='detail'),
    path('urls', custom_sitemap, name='url'),
    path('yandex/turbo', YandexTurbo.as_view(), name='turbo'),
    path('create', ParceObjects.as_view(), name='create')
]
