from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None)
def main_page(request):
    return render(request, 'weather/index.html')
