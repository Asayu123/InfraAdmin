from django.db import models


# Create your models here.

class DataCenter(models.Model):
    POS_CHOICES = (('front', 'フロント'), ('back', 'バック'))
    name = models.CharField(max_length=32, unique=True)
    usage = models.CharField(max_length=64, choices=POS_CHOICES)

    def __str__(self):
        return self.name


class VCenterCluster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    HA_available = models.BooleanField()
    belongDC = models.ForeignKey('DataCenter', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Rack(models.Model):
    name = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64, unique=True)
    max_slot = models.IntegerField(default=16)

    def __str__(self):
        return self.name


class RackPos(models.Model):
    belongs = models.ForeignKey('Rack', to_field='name')
    number = models.IntegerField()

    def __str__(self):
        return self.belongs


class HypervisorNodeTable(models.Model):
    nodename = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nodename


class HypervisorUsage(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class HypervisorHost(models.Model):
    # management data
    name = models.CharField(max_length=64, unique=True)
    nodename = models.OneToOneField('HypervisorNodeTable')
    belong_cluster = models.ForeignKey('VCenterCluster', to_field='name', on_delete=models.PROTECT)
    rackpos = models.ForeignKey('RackPos', to_field='id', on_delete=models.PROTECT)
    usage = models.ForeignKey('HypervisorUsage', to_field='name', on_delete=models.PROTECT)
    reserved = models.BooleanField(default=False)

    # specification
    cpu_core_num = models.IntegerField()
    memory_capacity = models.IntegerField()
    hdd_capacity = models.IntegerField()

    def __str__(self):
        return self.name


class NFSStorage(models.Model):
    pass


class NFSVolume(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    path = models.CharField(max_length=64, unique=True)
    capacity = models.PositiveIntegerField()  # Unit is GigaByte

    def __str__(self):
        return self.name


class VirtualMachineBase(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    # HDD and NIC information is stored in another class (i.e:Table)
    hostname = models.CharField(max_length=64, unique=True)
    usage = models.CharField(max_length=256)
    os = models.CharField(max_length=64)
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()  # Unit is GigaByte
    HA_required = models.BooleanField()
    note = models.CharField(max_length=1024)

    # following attribute is linked to another table.
    vmhost = models.ForeignKey('HypervisorHost', to_field='name', on_delete=models.PROTECT)
    software = models.ManyToManyField('VmInstalledSoftware')
    serverspec_tests = models.ManyToManyField('VmServerSpecTest')
    chef_recipes = models.ManyToManyField('VmChefRecipe')

    def __str__(self):
        return self.hostname


class VmAttachedVirtualHDD(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    vmID = models.IntegerField()  # vmID will be "id" that has been created in class "VirtualMachine"
    mount_point = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField()  # Unit is GigaByte will be Stored
    datastore = models.CharField(max_length=128)

    def __str__(self):
        return self.mount_point


class VmNetworkInfo(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    vmID = models.IntegerField()  # vmID will be "id" that has been created in class "VirtualMachine"
    vLAN_ID = models.PositiveIntegerField()
    IP_Address = models.GenericIPAddressField()

    def __str__(self):
        return self.IP_Address


class VmInstalledSoftware(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class VmServerSpecTest(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class VmChefRecipe(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
