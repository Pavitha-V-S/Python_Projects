from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from .forms import todoform
from . models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class tasklist(ListView):
    model=Task
    template_name='home.html'
    context_object_name = 'task'

class taskdetail(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class taskupdate(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class taskdelete(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')





def add(request):
    task = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        tasks=Task(name=name,priority=priority,date=date)
        tasks.save()
    return render(request,'home.html',{'task':task})
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')
def update(request,id):
    task=Task.objects.get(id=id)
    form=todoform(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'task':task})