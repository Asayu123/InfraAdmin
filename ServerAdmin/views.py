from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
#from django import forms

from django.http import *

from django.views.generic import TemplateView  # for class based views
from django.views.decorators.http import require_http_methods

from django.db.models import *
from django.db import IntegrityError

from ServerAdmin import models

from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from ServerAdmin import forms

# Create your views here.


class Default(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('index'))


class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


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


# Refer view starts Here
class ShowTableVM(TemplateView):

    def get_context_data(self):

        table_data = models.VirtualMachine.objects.all()
        return {'TableData': table_data}

    def get(self, request, name="default", *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'vm_list.html', context)


class ShowDetailVM(TemplateView):

    def get_context_data(self, hostname):
        vm = models.VirtualMachine.objects.get(name__exact=hostname)
        hdds = models.VmAttachedVirtualHDD.objects.filter(virtualmachine=vm)
        nics = models.VmAttachedVirtualNIC.objects.filter(virtualmachine=vm)

        return {"vm": vm, "hdds": hdds, "nics": nics}

    def get(self, request, *args, **kwargs):

        hostname = kwargs['hostname']
        query_results = self.get_context_data(hostname)
        context = {'hostname': hostname, 'vm': query_results["vm"],
                   'HDDs': query_results["hdds"], 'NICs': query_results["nics"]}

        return render(request, 'vm_detail.html', context)


class ShowTableHypervisor(TemplateView):

    def get_context_data(self):

        table_data = models.HypervisorHost.objects.all()
        return {'TableData': table_data}

    def get(self, request, name="default", *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'hypervisor_list.html', context)


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


class ShowTableNetwork(TemplateView):

    def get_context_data(self):
        table_data = models.Network.objects.all()

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'network_list.html', context)


class ShowDetailNetwork(TemplateView):

    def get_context_data(self, network):
        table_data = models.Network.objects.filter(name__exact=network)

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        network = kwargs["network"]
        context = self.get_context_data(network)
        return render(request, 'network_detail.html', context)


class ShowTableDnsRecord(TemplateView):

    def get_context_data(self):

        table_data = models.DnsRecord.objects.all()

        for table in table_data:
            if (table.priority == None):
                table.priority = "-"

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'dns_record_list.html', context)


class FormDnsRecord(TemplateView):

    def get(self, request, *args, **kwargs):

        form = forms.DnsRecordForm()
        context = {"form": form}
        context.update({"title": "Create Record"})
        context.update({"subtitle": "DNS Record"})

        return render(request, 'generic_form.html', context)


class CreateDnsRecord(TemplateView):
    pass


class ShowTableSecurityGroup(TemplateView):

    def get_context_data(self):
        table_data = models.SecurityGroup.objects.all()

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'security_group_list.html', context)


class ShowTableFirewall(TemplateView):

    def get_context_data(self):
        table_data = models.BoundaryFirewall.objects.all()

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        return render(request, 'boundary_firewall_list.html', context)


class ShowTableFirewallRulesSG(TemplateView):

    def get_context_data(self, security_group):
        table_data = models.FirewallRuleEntry.objects.filter(security_group__name__exact=security_group)

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        security_group = kwargs["security_group"]
        context = self.get_context_data(security_group)
        context.update({'SecurityGroup': security_group})

        return render(request, 'sg_rule_list.html', context)


class FormFirewallRules(TemplateView):

    def get(self, request, *args, **kwargs):

        security_group = kwargs["security_group"]
        form = forms.FirewallRuleForm()

        context = {"form": form}
        context.update({"title": "Create New Rule"})
        context.update({"subtitle": "for {0}".format(security_group)})
        context.update({"security_group": security_group})

        return render(request, 'generic_form.html', context)

    
class FormBoundaryFirewallRules(TemplateView):

    def get(self, request, *args, **kwargs):

        firewall = kwargs["firewall"]
        form = forms.FirewallRuleForm()

        context = {"form": form}
        context.update({"title": "Create New Rule"})
        context.update({"subtitle": "for {0}".format(firewall)})
        context.update({"security_group": firewall})

        return render(request, 'generic_form.html', context)


class ShowTableFirewallRulesBD(TemplateView):

    def get_context_data(self, firewall):
        table_data = models.FirewallRuleEntryBoundary.objects.filter(firewall__name__exact=firewall)

        return {'TableData': table_data}

    def get(self, request, *args, **kwargs):

        firewall = kwargs["firewall"]
        context = self.get_context_data(firewall)
        context.update({'Firewall': firewall})

        return render(request, 'fw_rule_list.html', context)


class ShowGenericTable(TemplateView):

    def get_context_data(self, model):
        cl = getattr(models, model)
        instance = cl()
        table_data = instance.objects.all()

        return {'TableData': table_data}

    def get(self, request, model="default", *args, **kwargs):
        context = self.get_context_data(model)
        return render(request, 'hypervisor_list.html', context)