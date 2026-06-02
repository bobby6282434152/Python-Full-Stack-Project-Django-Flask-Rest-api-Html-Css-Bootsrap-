from django.shortcuts import render,redirect
from .models import Todo
from .forms import TodoForm
# Create your views here.
def home(request):
    todos = Todo.objects.all()
    return render(request, 'home.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    else:
        form = TodoForm()
        return render(request, 'add_todo.html', {'form': form})
    
def update_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm(instance=todo)
        return render(request, 'update_todo.html', {'form': form})
    
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    return render(request, 'delete_todo.html', {'todo': todo})