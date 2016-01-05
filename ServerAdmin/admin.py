from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.DataCenter)
admin.site.register(models.VCenterCluster)
admin.site.register(models.RackPos)
admin.site.register(models.HypervisorNodeTable)
admin.site.register(models.HypervisorUsage)
admin.site.register(models.HypervisorHost)
admin.site.register(models.NFSStorage)
admin.site.register(models.NFSVolume)
admin.site.register(models.VirtualMachineBase)
admin.site.register(models.VmAttachedVirtualHDD)
admin.site.register(models.VmNetworkInfo)
admin.site.register(models.VmInstalledSoftware)
admin.site.register(models.VmServerSpecTest)
admin.site.register(models.VmChefRecipe)