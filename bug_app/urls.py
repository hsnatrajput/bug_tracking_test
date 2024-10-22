from django.urls import path
from . import views
from .views import  bug_delete_view , BugStatusUpdateView
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('bugs/create/<int:project_id>', views.create_project_bug, name="create_project_bug"),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('bug/<int:pk>/delete/', bug_delete_view.as_view(), name='bug_delete_view'),
    path('bug/<int:pk>/status_update/', BugStatusUpdateView.as_view(), name='bug_status_update'),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
