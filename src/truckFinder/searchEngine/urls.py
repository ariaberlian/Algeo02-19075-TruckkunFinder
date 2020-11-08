from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('howto/', views.how_to_use, name="howto"),
    path('concept/', views.concept, name="concept")
]
app_name = 'searchEngine'