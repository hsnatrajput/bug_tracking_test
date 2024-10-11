from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Bug, Project, Screenshot , User
from .forms import BugForm, ScreenshotForm, ProjectForm , UserForm
from django.contrib.auth import login ,  authenticate, logout
from django.views.generic import DeleteView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy 
from django .db.models import Q , Count
from django.core.paginator import Paginator

def signup(request):
    user_type = request.GET.get('user_type') 
    if not user_type:
        return redirect('home')  
    if request.method == 'POST':
        form = UserForm(request.POST, user_type=user_type)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = UserForm(user_type=user_type)  

    return render(request, 'hasnat_app/signup.html', {'form': form, 'user_type': user_type})


def user_login(request):
    error_message = None  

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('project_list')  
        else:
            error_message = 'Invalid username or password'  

    return render(request, 'hasnat_app/login.html', {'error': error_message})  


def logout_success(request):
    return render(request, 'hasnat_app/logout.html')


@login_required
def dashboard(request):
    return render(request, 'hasnat_app/dashboard.html', { 'user': request.user})




@login_required(login_url='login') 
def project_list(request):
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
    return render(request, 'hasnat_app/project_list.html', context)




@login_required
def create_project(request):
    if request.user.user_type != 'manager':
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

    return render(request, 'hasnat_app/create_project.html', {'form': form})

@login_required(login_url='login') 
def bug_list(request):
    bugs = Bug.objects.all()
    return render(request, 'hasnat_app/bug_list.html', {'bugs': bugs})
from django.contrib.auth import get_user_model

@login_required
def create_bug(request , project_id ):
    # print("**********************",project_id)
    project = get_object_or_404(Project , id=project_id)
    # print(f"Project ID: {project.id}") 
    # project = Project.objects.get(id=project_id)
    User = get_user_model()

    
    if request.user.user_type not in ['manager', 'qa']:
        return render(request, 'hasnat_app/error.html', {
            'message': 'You do not have permission to create a bug.'
        })

    if request.method == 'POST':
        bug_form = BugForm(request.POST)
        screenshot_form = ScreenshotForm(request.POST, request.FILES)

        if bug_form.is_valid() and screenshot_form.is_valid():
            bug = bug_form.save(commit=False)
            bug.reported_by = request.user
            bug.project = project  
            # bug.project_id = project_id
            bug.save()

      
            for img in request.FILES.getlist('image'):
                screenshot = Screenshot(image=img, bug=bug)
                screenshot.save()

            return redirect('project_detail', project_id=project.id)
        else:
      
            print(bug_form.errors)
            print(screenshot_form.errors)

    else:
       
        bug_form = BugForm(initial={'project': project.id}, user=request.user) 
        screenshot_form = ScreenshotForm()

  
    users = User.objects.all()

    return render(request, 'hasnat_app/project_detail.html', {
        'bug_form': bug_form,
        'screenshot_form': screenshot_form,
        'project': project,
        'users': users,  
    })



# def home(request):
#     return render(request, 'hasnat_app/home.html')

class bug_delete_view(DeleteView):
    model = Bug
    template_name = 'hasnat_app/delete_bug.html' 
    context_object_name = 'bug'
    success_url = reverse_lazy('project_detail') 

    def get_success_url(self):
       
        project_id = self.object.project.id
        return reverse_lazy('project_detail', kwargs={'project_id': project_id})

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type not in ['manager', 'qa']:
            return render(request, 'hasnat_app/error.html')  
        return super().dispatch(request, *args, **kwargs)



class BugStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    fields = ['status']
    template_name = 'hasnat_app/bug_status_update.html'
    
    def get_success_url(self):
       
        project_id = self.object.project.id
        return reverse_lazy('project_detail', kwargs={'project_id': project_id})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.user_type != 'developer':
            return render(request, 'hasnat_app/error.html')
        
        return super().dispatch(request, *args, **kwargs)


    
def screenshot(request):
    if request.method == 'POST':
        form = ScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.getlist('image')  
            for img in image:
                Screenshot.objects.create(image=img)  
            

    else:
        form = ScreenshotForm()

    image = Screenshot.objects.all()
    return render(request, 'hasnat_app/create_bug.html', {'form': form, 'image': image})
      


def home(request):
    return render(request, 'hasnat_app/home.html')

# def project_bugs(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     bugs = project.bugs.all()  
#     return render(request, 'hasnat_app/project_bugs.html', {'project': project, 'bugs': bugs})



@login_required(login_url='login') 
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # print(f"Project ID: {project.id}") 
    query = request.GET.get('q')  
    if query:
        bugs = Bug.objects.filter(
            project=project
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        # bugs = Bug.objects.filter(id=project_id)
        bugs = Bug.objects.filter(project=project)
        

  
    users = User.objects.filter(user_type='developer')

    context = {
        'project': project,
        'users': users,
        'projects': Project.objects.all(),
        'bugs': bugs,
    }
    return render(request, 'hasnat_app/project_detail.html', context)
    