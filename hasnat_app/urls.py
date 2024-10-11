from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import bug_delete_view , BugStatusUpdateView
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    # path('', views.home, name='home'), 
    path('', views.project_list, name='project_list'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_success'), name='logout'),
    
    
    path('logout_success/', views.logout_success, name='logout_success'), 

    path('dashboard/', views.dashboard, name='dashboard'),

   
    path('projects/create/', views.create_project, name='create_project'),
    path('', views.project_list, name='project_list'),
    
    
    path('bugs/create/', views.create_bug, name='create_bug'),
    path('bugs/', views.bug_list, name='bug_list'),
    path('bug/<int:pk>/delete/', bug_delete_view.as_view(), name='bug_delete_view'),
    path('bug/<int:pk>/status_update/', BugStatusUpdateView.as_view(), name='bug_status_update'),
    path('home/', views.home, name='home'),
    
    
 

    path('projects/<int:project_id>/', views.project_detail, name='project_detail')
    



] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
