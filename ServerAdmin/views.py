from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import forms

from django.http import *

from django.views.generic import TemplateView  # for class based views
from django.views.decorators.http import require_http_methods

from django.db.models import *
from django.db import IntegrityError

from ServerAdmin import models

from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

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


class TestURL(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request,'base_inherit_test.html',context=None)


class CreateVM(CreateView):

    model = models.VirtualMachine
    success_url = reverse_lazy('vm_create')
    fields = ['name', 'usage', 'os', 'cpu', 'memory', 'HA_required',
              'hypervisorhost', 'vminstalledsoftware', 'vmserverspectest', 'vmchefrecipe']
    template_name = 'vm_form.html'

    def form_valid(self, form):
        try:
            return super(CreateVM, self).form_valid(form)
        except IntegrityError:
            return HttpResponse("error")  # Under Construction

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")  # Under Construction


class ShowTableVM(TemplateView):

    def get_context_data(self):

        table_data = models.VirtualMachine.objects.all()
        return {'TableData': table_data}

    def get(self, request, name="default", *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'vm_table.html', context)


class ShowDetailVM(TemplateView):

    def get_context_data(self, hostname):
        vm = models.VirtualMachine.objects.filter(name__exact=hostname)
        hdds = models.VmAttachedVirtualHDD.objects.filter(virtualmachine_name__exact=hostname)
        nics = models.VmAttachedVirtualNIC.objects.filter(virtualmachine_name__exact=hostname)

        return {"vm": vm, "hdds": hdds, "nics": nics}

    def get(self, request, *args, **kwargs):

        hostname = kwargs['hostname']
        query_results = self.get_context_data(hostname)
        context = {'hostname': hostname, 'VMs': query_results["vm"],
                   'HDDs': query_results["hdds"], 'NICs': query_results["nics"]}

        return render(request, 'vm_detail.html', context)


class ShowTableHypervisor(TemplateView):

    def get_context_data(self):

        table_data = models.HypervisorHost.objects.all()
        return {'TableData': table_data}

    def get(self, request, name="default", *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'hypervisor_table.html', context)


class ShowDetailHypervisor(TemplateView):

    def get_context_data(self, hostname):

        hv = models.HypervisorHost.objects.get(name__exact=hostname)
        vms = models.VirtualMachine.objects.filter(hypervisorhost=hv)  # return a queryset, a list.

        return {'hv': hv, 'vms': vms}

    def get(self, request, *args, **kwargs):

        hostname = kwargs['hostname']
        query_results = self.get_context_data(hostname)

        context = {'hostname': hostname, 'Hypervisor': query_results['hv'],'VMs': query_results['vms']}

        return render(request, 'hypervisor_detail.html', context)