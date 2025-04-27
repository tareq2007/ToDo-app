from django.urls import path
from . import views
from .views import TaskList, TaskDetail,TaskCreate,TaskUpdate,TaskDelete, CustomLoginView, RegisterView



urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    
    path('', TaskList.as_view(), name='task_list'),
    path('task-detail/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('create-task', TaskCreate.as_view(), name='create-task'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),


]   