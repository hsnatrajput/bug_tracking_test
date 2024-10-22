from django.urls import path
from . import views 
from.views import create_project , project_list
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
      path('', views.project_list, name='project_list'),
      path('projects/create/', views.create_project, name='create_project'),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
