from django.shortcuts import render
from django.views.generic.list import ListView

from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task_list')
    
def logoutUser(request):
    logout(request)
    return redirect('login')

class RegisterView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)




class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'todo/landing.html'
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed= False).count()
        context['completed_count'] = context['tasks'].filter(completed= True).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        return context

            


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task_list')
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'todo/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')
    