from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import forms

from django.views.generic import TemplateView  # for class based views
from django.views.decorators.http import require_http_methods

from ServerAdmin import models

# Create your views here.




class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


def index(request):  # func based view, not recommended in Django

    context = {"form": NameForm()}
    return render(request, 'index.html', context)


class IndexPage(TemplateView):  # class based view. for new standard.

    def get(self, request, *args, **kwargs):
        context = {"form": NameForm()}
        return render(request, 'index.html', context)


class ShowTable(TemplateView):

    def get_context_data(self, **kwargs):

        try:
            #target_table = kwargs['name']
            table_data = models.VirtualMachine.objects.all()
            return {'TableData': table_data}
        except:
            raise TypeError('requires table name as string, for argument')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request,'tables.html', context)


