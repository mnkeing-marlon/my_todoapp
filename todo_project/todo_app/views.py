from pickle import FALSE

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task



def task_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            user=request.user,
            completed=False
        )
        return redirect('task_list')


    return render(request, 'task_form.html')


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})

def task_toggle(request,pk):
    task = get_object_or_404(Task, pk=pk)
    if task.completed :
        task.completed = False
    else:
        task.completed = True

    task.save()
    return render(request, 'task_detail.html', {'task': task})




def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)


    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.completed = 'completed' in request.POST
        task.due_date = request.POST.get('due_date', '')
        task.due_time = request.POST.get('due_time', '')

        task.save()
        return redirect('task_list')

    return render(request, 'task_form.html', {'task': task})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return redirect('task_list')