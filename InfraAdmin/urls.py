"""InfraAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from ServerAdmin import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^VirtualMachine/Create/$', views.CreateVM.as_view(),name='vm_create'),  # Retrieve
    url(r'^VirtualMachine/$',views.ShowTableVM.as_view(), name='vm_list'),  # Retrieve
    url(r'^VirtualMachine/(?P<hostname>[A-z]+[0-9]+.+)', views.ShowDetailVM.as_view(), name='vm_detail'),  # Retrieve

    url(r'^Hypervisor/$', views.ShowTableHypervisor.as_view(),name='hv_list'),  # Retrieve
    url(r'^Hypervisor/(?P<hostname>[A-z]+[0-9]+.+)', views.ShowDetailHypervisor.as_view(), name='hv_detail'),  # Retrieve

    url(r'^Network/$', views.ShowTableNetwork.as_view(), name='network_list'),
    url(r'^Network/(?P<network>.+)', views.ShowDetailNetwork.as_view(), name='network_detail'),

    url(r'^DnsRecord/$', views.ShowTableDnsRecord.as_view(), name='dns_record_list'),
    url(r'^DnsRecord/Form$', views.FormDnsRecord.as_view(), name='dns_record_form'),
    url(r'^DnsRecord/Create$', views.CreateDnsRecord.as_view(), name='dns_record_form'),

    url(r'^SecurityGroup/(?P<security_group>.+)/Form$', views.FormFirewallRules.as_view(), name='firewall_rule_form'),  # Retrieve
    url(r'^SecurityGroup/(?P<security_group>.+)/*$', views.ShowTableFirewallRulesSG.as_view(), name='sg_rule_list'),  # Retrieve

    url(r'^Firewall/(?P<firewall>.+)/Form$', views.FormBoundaryFirewallRules.as_view(), name='bd_fw_rule_list'),
    url(r'^Firewall/(?P<firewall>.+)', views.ShowTableFirewallRulesBD.as_view(), name='fw_rule_list'),# Retrieve

    url(r'^SecurityGroup/$', views.ShowTableSecurityGroup.as_view(), name='security_group_list'),  # Retrieve

    url(r'^Firewall/$', views.ShowTableFirewall.as_view(), name='boundary_firewall_list'),  # Retrieve

    url(r'^model_(?P<model>[A-z,0-9]+)/$', views.ShowGenericTable.as_view(), name='generic_table'),  # Retrieve
]