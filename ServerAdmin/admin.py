from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from . import models

# Register your models here.

admin.site.register(models.Environment)
admin.site.register(models.DataCenter)
admin.site.register(models.VCenterClusterUsage)
admin.site.register(models.VCenterCluster)
admin.site.register(models.Rack)
admin.site.register(models.PhysicalServer)
admin.site.register(models.HypervisorHost)
admin.site.register(models.Datastore)
admin.site.register(models.NFS_Storage)
admin.site.register(models.VLAN)
admin.site.register(models.VirtualMachine)
admin.site.register(models.VmAttachedVirtualHDD)
admin.site.register(models.VmAttachedVirtualNIC)
admin.site.register(models.VmInstalledSoftware)
admin.site.register(models.VmServerSpecTest)
admin.site.register(models.VmChefRecipe)


# define Class for import-export module


class VCenterClusterUsageResource(resources.ModelResource):

    class Meta:
        model = models.VCenterClusterUsage


# define Classes for import-export django-admin integration
class ImportExportModule(ImportExportModelAdmin):
    resource_class = VCenterClusterUsageResource
    pass