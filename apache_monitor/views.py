from django.shortcuts import render
from .models import RemoteHost


def index(request):
    context = {}
    return render(request, 'apache_monitor/index.html', context)

def hosts(request):
    all_hosts = RemoteHost.objects.all()
    context = {'all_hosts': all_hosts}
    return render(request, 'apache_monitor/hosts.html', context)