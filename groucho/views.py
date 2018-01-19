from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from groucho.forms import LoginForm
from groucho.helpers import get_source_ip


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, source_ip=get_source_ip(request))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groucho-login'))
    else:
        form = LoginForm()

    return render(request, 'groucho/login.html', {'form': form})

