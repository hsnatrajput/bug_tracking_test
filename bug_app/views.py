from django.shortcuts import render , redirect ,get_object_or_404
from django.views.generic import DeleteView , UpdateView
from .models import Bug,  Screenshot 
from django.urls import reverse_lazy 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from project_app.models import Project
from .forms import BugForm 
from django .db.models import Q 
from hasnat_app.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

class bug_delete_view(DeleteView):
    model = Bug
    template_name = 'bug_app/delete_bug.html'
    context_object_name = 'bug'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type not in ['manager', 'qa']:
            return JsonResponse({'success': False, 'error': 'You do not have permission to delete this bug.'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


class BugStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()     
        try:
            data = json.loads(request.body)
            status = data.get('status')  
            if status:
                self.object.status = status  
                self.object.save()  
                return JsonResponse({'success': True})  
            else:
                return JsonResponse({'success': False, 'error': 'No status provided.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'})
  

def create_project_bug(request, project_id): 
    if request.user.user_type not in ['manager', 'qa']:
        return render(request, 'hasnat_app/error.html') 
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        form.cleaned_data = {
                'title': request.POST.get('title'),
                'description': request.POST.get('description'),
                'deadline': request.POST.get('deadline'),
                'type': request.POST.get('type'),
                'status': request.POST.get('status'),
                'assigned_to': request.POST.get('assigned_to')
            }
        bug = Bug(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            deadline=form.cleaned_data['deadline'],
            type=form.cleaned_data['type'],
            status='new',
            assigned_to_id=form.cleaned_data['assigned_to'],
            project=project,
            reported_by=request.user
        )
        bug.save()
        files = request.FILES.getlist('image')
        for file in files:
            Screenshot.objects.create(bug=bug, image=file)
        return redirect('project_detail', project_id=project.id)

        
@login_required(login_url='login')
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    query = request.GET.get('q')  
    if query:
        bugs = Bug.objects.filter(
            project=project
        ).filter(
            Q(title__icontains=query) 
        )
    else:
        bugs = Bug.objects.filter(project=project)
    users = User.objects.filter(user_type='developer')  
    context = {
        'project': project,
        'users': users, 
        'projects': Project.objects.all(),
        'bugs': bugs,
    }
    return render(request, 'bug_app/project_detail.html', context)

