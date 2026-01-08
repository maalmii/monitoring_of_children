from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ditina
from .forms import DitinaForm
from .views_graph import random_graph


def home_page_view(request):
    return render(request, 'home.html')

def about_page_view(request):
    return render(request, 'about.html')

def register_page_view(request):
    return render(request, 'register.html')

def login_page_view(requset):
    return render(requset, 'login.html')


#@login_required
def dashboard_page_view(request):
    form_submitted = False
    if request.method == 'POST':
        form = DitinaForm(request.POST)
        form_submitted = True
        if form.is_valid():
            form.save()
            messages.success(request, 'Informacja o dziecku została pomyślnie dodana!')
            return redirect('dashboard')
    else:
        form = DitinaForm()

    dity_list = Ditina.objects.all()

    context = {
        'form': form,
        'dity_list': dity_list,
        'form_submitted': form_submitted,
    }
    return render(request, 'dashboard.html', context)


def edit_ditina_view(request, ditina_id):
    ditina = Ditina.objects.get(id=ditina_id)
    if request.method == 'POST':
        form = DitinaForm(request.POST, instance=ditina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informacja o dziecku została zaktualizowana!')
            return redirect('dashboard')
    else:
        form = DitinaForm(instance=ditina)
    dity_list = Ditina.objects.all()
    context = {
        'form': form,
        'dity_list': dity_list,
        'edit_mode': True,
        'edit_id': ditina_id,
    }
    return render(request, 'dashboard.html', context)

def delete_ditina_view(request, ditina_id):
    ditina = Ditina.objects.get(id=ditina_id)
    if request.method == 'POST':
        ditina.delete()
        messages.success(request, 'Rekord dziecka został usunięty!')
        return redirect('dashboard')
    return redirect('dashboard')