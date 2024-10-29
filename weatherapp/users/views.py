from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    register_form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if register_form.is_valid():
            print('Valid!')
            register_form.save()
            return redirect('login/')
    
    return render(request, 'users/register.html', {'form': register_form})


