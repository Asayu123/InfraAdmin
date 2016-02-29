from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import forms

from django.http import Http404

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

        hv = models.HypervisorHost.objects.filter(name__exact=hostname)
        vms = models.VirtualMachine.objects.filter(hypervisorhost_name__exact=hostname)

        return {"hv": hv, "vms": vms}

    def get(self, request, *args, **kwargs):

        hostname = kwargs['hostname']
        query_results = self.get_context_data(hostname)
        context = {'hostname': hostname, 'HV': query_results["hv"],'VMs': query_results["vms"]}

        return render(request, 'hypervisor_detail.html', context)