from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_command, name='analyze_command'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('sheet-data/<str:sheet_name>/', views.get_sheet_data, name='get_sheet_data'),
    path('generate-graph/', views.generate_graph, name='generate_graph'),
    # ...autres vues...
]

# Add media URL pattern for serving uploaded files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)