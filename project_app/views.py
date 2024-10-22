from django.shortcuts import render , redirect
from django .db.models import Q , Count
from django.core.paginator import Paginator
from.models import Project
from hasnat_app.models import User
from django.contrib.auth.decorators import login_required 
from .forms import ProjectForm


@login_required(login_url='login') 
def project_list(request):
    projects = Project.objects.all
    query = request.GET.get('q')  
    if query:
        projects = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).annotate(
            total_bugs=Count('bugs'),
            done_tasks=Count('bugs', filter=Q(bugs__status__in=['resolved', 'completed']))  
        )
    else:
        projects = Project.objects.all().annotate(
            total_bugs=Count('bugs'),
            done_tasks=Count('bugs', filter=Q(bugs__status__in=['resolved', 'completed']))  
        )     
    paginator = Paginator(projects, 6) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    users = User.objects.filter(user_type='developer')
    context = {
        'page_obj': page_obj,
        'projects': page_obj.object_list, 
        'form': ProjectForm(),
        'users': users 
    }
    return render(request, 'project_app/project_list.html', context)


@login_required
def create_project(request):
    if request.user.user_type not in ['manager']:
        return render(request, 'hasnat_app/error.html') 
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user  
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_app/create_project.html', {'form': form})