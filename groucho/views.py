from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDay
from groucho.forms import LoginForm
from groucho.helpers import get_source_ip
from groucho.models import AttemptSource


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, source_ip=get_source_ip(request))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groucho-login'))
    else:
        form = LoginForm()

    return render(request, 'groucho/login.html', {'form': form})


@login_required
def source_history(request):
    days = []
    history_queryset = None
    if request.GET.get('ip'):
        history_queryset = AttemptSource.objects.filter(ip=request.GET.get('ip'))
    else:
        history_queryset = AttemptSource.objects

    for day in history_queryset.annotate(day=TruncDay('created')).values('day').annotate(Count('day')).order_by('day')[:20]:
        days.append({
            'day': day['day'].strftime('%b %d, %Y'),
            'requests': day['day__count']
        })

    return JsonResponse({'days': days})