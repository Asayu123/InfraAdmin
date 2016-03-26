from django.db import models
from django.core import validators
import uuid


# Base Model Here

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.


class Environment(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class DataCenter(BaseModel):

    name = models.CharField(max_length=32, unique=True)
    environment = models.ForeignKey('Environment', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class VCenterCluster(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    usage = models.CharField(max_length=128)
    HA_available = models.BooleanField()
    DataCenter = models.ForeignKey('DataCenter', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Rack(BaseModel):
    name = models.CharField(max_length=64, unique=True)  # for human readable name
    serial = models.CharField(max_length=128)
    console = models.CharField(max_length=64, blank=True)  # string, match to node number,console number
    environment = models.ForeignKey('Environment', on_delete=models.PROTECT)
    num_of_unit = models.IntegerField(default=32)

    def __str__(self):
        return self.name


class PhysicalServerProduct(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class PhysicalServer(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    serial = models.CharField(max_length=64, unique=True)
    product = models.ForeignKey('PhysicalServerProduct', on_delete=models.PROTECT)
    environment = models.ForeignKey('Environment', on_delete=models.PROTECT)

    # specification
    cpu_core_num = models.PositiveIntegerField(help_text="[Core]") #Core
    cpu_socket_num = models.PositiveIntegerField(help_text="use this field for License Evaluation")
    memory_capacity = models.PositiveIntegerField(help_text="[GB]")  # GigaByte
    hdd_capacity = models.PositiveIntegerField(help_text="[GB]")  # GigaByte

    # following info is used when visualizing server layout
    rack = models.ForeignKey('Rack', on_delete=models.PROTECT)
    rack_unit_start = models.PositiveIntegerField()
    rack_unit_end = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class HypervisorHost(BaseModel):
    # management data
    name = models.CharField(max_length=64, unique=True)
    reserved = models.BooleanField(default=False)

    cpu_core_num_for_vm = models.PositiveIntegerField(null=False, help_text="[Core]")
    memory_capacity_for_vm = models.PositiveIntegerField(null=False, help_text="[GB]")
    hdd_capacity_for_vm = models.PositiveIntegerField(null=False, help_text="[GB]")

    # reference
    vCenterCluster = models.ForeignKey('VCenterCluster', on_delete=models.PROTECT)
    PhysicalServer = models.OneToOneField('PhysicalServer', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Datastore(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    storage = models.ForeignKey('Volume', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Volume(BaseModel):  # Use this table to define NFS Volumes
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    storage = models.ForeignKey('nfs_storage', on_delete=models.PROTECT)
    path = models.CharField(max_length=128)
    capacity = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte

    def __str__(self):
        return self.name + ':' + self.description


class nfs_storage(BaseModel):  # Use this table to define storage such as NFS
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    ipaddr = models.GenericIPAddressField()
    capacity = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte

    def __str__(self):
        return self.name + ':' + self.description


class VLAN(BaseModel):  # Define Relationship between VLANID , Usage , IPRange
    VLAN_ID = models.IntegerField(unique=True)
    usage = models.CharField(max_length=256)
    nwaddr = models.GenericIPAddressField()
    prefix = models.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(128)])

    def __str__(self):
        return str(self.VLAN_ID) + ':' + self.usage


class OperatingSystem(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class VirtualMachine(BaseModel):
    # HDD and NIC information is stored in another schema (i.e:List / Table)
    name = models.CharField(max_length=64, unique=True)
    usage = models.CharField(max_length=256)
    os = models.ForeignKey('OperatingSystem', on_delete=models.PROTECT)
    cpu = models.PositiveIntegerField(help_text="[core]")
    memory = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte
    HA_required = models.BooleanField()

    # following attribute is linked to another table.

    hypervisorhost = models.ForeignKey('HypervisorHost', on_delete=models.PROTECT)
    vminstalledsoftware = models.ManyToManyField('VmInstalledSoftware')
    vmserverspectest = models.ManyToManyField('VmServerSpecTest')
    vmchefrecipe = models.ManyToManyField('VmChefRecipe')


    def __str__(self):
        return self.name


class VmAttachedVirtualHDD(BaseModel):
    virtualmachine = models.ForeignKey('VirtualMachine', on_delete=models.CASCADE)
    mount_point = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte will be Stored
    datastore = models.ForeignKey('Datastore', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.virtualmachine.name)


class VmAttachedVirtualNIC(BaseModel):
    virtualmachine = models.ForeignKey('VirtualMachine', on_delete=models.CASCADE)
    vLAN_ID = models.ForeignKey('VLAN', on_delete=models.PROTECT)
    IP_Address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.virtualmachine.name)


class VmInstalledSoftware(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class VmServerSpecTest(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class VmChefRecipe(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Write Application Model Here

class VirtualMachineDetail:

    def __init__(self,hostname):
        self.hostname = hostname
