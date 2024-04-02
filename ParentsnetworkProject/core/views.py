from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.edit import CreateView , UpdateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.utils.decorators import method_decorator
from .forms import *
from django.contrib import messages


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('profile')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super(SignupView,self).get(*args,**kwargs)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == "GET":
            return render(request,'login.html')
        elif request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('profile')
            else:
                print("wrong username or password")
                return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')


@method_decorator(login_required(login_url='login'),name='dispatch')
class AccountSettingsView(UpdateView):
    model = User
    fields = ['first_name','last_name','profile_pic','bio']
    template_name = 'account_settings.html'
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user
    

def addParent(request):
    user = User.objects.filter(is_superuser=False)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Parent Added Successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please Fill the Form Correctly')
    else:
        form = UserForm()
    context = {'user':user, 'form': form}
    return render(request, 'addParent.html', context)


def deleteParent(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('addParent')

def toDoList(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    context = {'tasks': tasks}
    return render(request, 'toDoList.html', context)


def addTask(request):
    user = request.user
    if request.method == 'POST':
        form = TaskForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('toDoList')  # Redirect to the toDoList view
    else:
        form = TaskForm(user=user)

    context = {'form': form}
    return render(request, 'toDoList.html', context)


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('toDoList')


def show_parent_schedule(request, pk):
    objs = Schedule.objects.filter(parent__id = pk)
    return render(request, 'schedule.html', {"objs": objs})


def all_schedule(request):
    user = User.objects.filter(is_superuser=False)
    context = {'user':user}
    return render(request, 'all_schedule.html', context)


def edit_schedule(request, pk):
    schedule_instance = Schedule.objects.get(id=pk)
    parent_id = schedule_instance.parent.id
    
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule_instance)
        if form.is_valid():
            form.save()
            return redirect(manage_parent_schedule, pk=parent_id)
    else:
        form = ScheduleForm(instance=schedule_instance)

    context = {'form': form}
    return render(request, 'edit_schedule.html', context)


def manage_parent_schedule(request, pk):
    parent_schedule = Schedule.objects.filter(parent__id = pk)
    user = User.objects.filter(is_superuser=False)
    context = {'user':user, 'parent_schedule': parent_schedule}
    return render(request, 'manage_parent_schedule.html', context)


def contact_parent(request):
    user = User.objects.filter(is_superuser=False)
    context = {'user':user}
    return render(request, 'contact.html', context)



def contact_admin(request):

    return render(request, 'contact_admin.html')