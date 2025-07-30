from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_command, name='analyze_command'),
    path('chart/demandes-per-categorie/', views.demandes_per_categorie_chart, name='demandes_per_categorie_chart'),
    # ...autres vues...
]