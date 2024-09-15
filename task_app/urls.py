from django.urls import path
from . import views

urlpatterns = [
    # List all tasks for the authenticated user
    path('tasks/', views.TaskListView.as_view(), name='task-list'),

    # Create a new task
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),

    # Retrieve details of a specific task by its primary key
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # Update an existing task by its primary key
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),

    # Delete a task by its primary key
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    # Filter tasks based on their status
    path('tasks/filter/', views.TaskFilterView.as_view(), name='task-filter'),
]
