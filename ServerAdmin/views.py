from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.views.decorators.http import require_http_methods

# Create your views here.

def index(request):
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)

    context = { "form" : NameForm() }

    return render(request, 'bootstrap_demo.html', context)