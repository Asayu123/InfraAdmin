from django import forms
from ServerAdmin import models


class DnsRecordForm(forms.ModelForm):
    class Meta:
        model = models.DnsRecord
        fields = ['name', 'type', 'data', 'ttl', 'priority']


class FirewallRuleForm(forms.ModelForm):

    class Meta:
        model = models.FirewallRuleEntryBoundary
        fields = ['name', 'direction', 'network', 'protocol', 'port_range', 'firewall']
        widgets = {'firewall': forms.HiddenInput()}