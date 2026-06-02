from django.urls import path
from . import views
urlpatterns = [
path('', views.home, name='home'),
path('add/', views.add_todo, name='add_todo'),
path('update/<int:todo_id>/', views.update_todo, name='update_todo'),
path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
