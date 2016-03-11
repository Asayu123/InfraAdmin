from django.db import models
from django.core import validators

# Create your models here.


class Environment(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name


class DataCenter(models.Model):

    name = models.CharField(max_length=32, primary_key=True)
    environment_name = models.ForeignKey('Environment', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class VCenterClusterUsage(models.Model):  # for example , "frontend" "backend" "db" etc...
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class VCenterCluster(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    VCenterClusterUsage_name = models.ForeignKey('VCenterClusterUsage', to_field='name', on_delete=models.PROTECT)
    HA_available = models.BooleanField()
    DataCenter_name = models.ForeignKey('DataCenter', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Rack(models.Model):
    name = models.CharField(max_length=64, primary_key=True)  # for human readable name
    serial = models.CharField(max_length=128, unique=True)
    console_name = models.CharField(max_length=64, unique=True)  # string, match to node number,console number
    environment_name = models.ForeignKey('Environment', to_field='name', on_delete=models.PROTECT)
    num_of_unit = models.IntegerField(default=32)

    def __str__(self):
        return self.name


class PhysicalServerProduct(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class PhysicalServer(models.Model):
    serial = models.CharField(max_length=64, primary_key=True)
    product_name = models.ForeignKey('PhysicalServerProduct', to_field='name', on_delete=models.PROTECT)
    environment_name = models.ForeignKey('Environment', to_field='name', on_delete=models.PROTECT)

    # specification
    cpu_core_num = models.PositiveIntegerField(help_text="[Core]") #Core
    cpu_socket_num = models.PositiveIntegerField(help_text="use this field for License Evaluation")
    memory_capacity = models.PositiveIntegerField(help_text="[GB]")  # GigaByte
    hdd_capacity = models.PositiveIntegerField(help_text="[GB]")  # GigaByte

    # following info is used when visualizing server layout
    rack_name = models.ForeignKey('Rack', to_field='name', on_delete=models.PROTECT)
    rack_unit_start = models.PositiveIntegerField()
    rack_unit_end = models.PositiveIntegerField()

    # following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return self.serial


class HypervisorHost(models.Model):
    # management data
    name = models.CharField(max_length=64, primary_key=True)
    reserved = models.BooleanField(default=False)

    cpu_core_num_for_vm = models.PositiveIntegerField(null=False, help_text="[Core]")
    memory_capacity_for_vm = models.PositiveIntegerField(null=False, help_text="[GB]")
    hdd_capacity_for_vm = models.PositiveIntegerField(null=False, help_text="[GB]")

    # following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    # reference
    vCenterCluster_name = models.ForeignKey('VCenterCluster', to_field='name', on_delete=models.PROTECT)
    PhysicalServer_serial = models.OneToOneField('PhysicalServer', to_field='serial', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Datastore(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class NFS_Storage(models.Model):  # Use this table to define NFS Datastore's network Path.
    datastore_name = models.OneToOneField('Datastore', to_field='name', primary_key=True, on_delete=models.PROTECT)
    ipaddr = models.GenericIPAddressField()
    path = models.CharField(max_length=128)
    capacity = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte

    def __str__(self):
        return str(self.datastore_name)  # if we want to return foreignkey, need to cast string object.


class VLAN(models.Model):  # Define Relationship between VLANID , Usage , IPRange
    id = models.IntegerField(primary_key=True, validators=[validators.MinValueValidator(0),validators.MaxValueValidator(4096)])
    usage = models.CharField(max_length=256)
    nwaddr = models.GenericIPAddressField()
    prefix = models.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(32)])

    def __str__(self):
        return str(self.id)


class OperatingSystem(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name


class VirtualMachine(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    # HDD and NIC information is stored in another schema (i.e:List / Table)
    name = models.CharField(max_length=64, primary_key=True)
    usage = models.CharField(max_length=256)
    os = models.ForeignKey('OperatingSystem', to_field='name', on_delete=models.PROTECT)
    cpu = models.PositiveIntegerField(help_text="[core]")
    memory = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte
    HA_required = models.BooleanField()

    # following attribute is linked to another table.

    hypervisorhost_name = models.ForeignKey('HypervisorHost', to_field='name', on_delete=models.PROTECT)
    vminstalledsoftware_name = models.ManyToManyField('VmInstalledSoftware')
    vmserverspectest_name = models.ManyToManyField('VmServerSpecTest')
    vmchefrecipe_name = models.ManyToManyField('VmChefRecipe')

    # following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return self.name


class VmAttachedVirtualHDD(models.Model):
    id = models.AutoField(primary_key=True)
    virtualmachine_name = models.ForeignKey('VirtualMachine', to_field='name', on_delete=models.CASCADE)
    mount_point = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField(help_text="[GB]")  # Unit is GigaByte will be Stored
    datastore_name = models.ForeignKey('Datastore', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.virtualmachine_name)


class VmAttachedVirtualNIC(models.Model):
    id = models.AutoField(primary_key=True)
    virtualmachine_name = models.ForeignKey('VirtualMachine', to_field='name', on_delete=models.CASCADE)
    vLAN_id = models.ForeignKey('VLAN', to_field='id', on_delete=models.PROTECT)
    IP_Address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.virtualmachine_name)


class VmInstalledSoftware(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class VmServerSpecTest(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class VmChefRecipe(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


# Write Application Model Here

class VirtualMachineDetail:

    def __init__(self,hostname):
        self.hostname = hostname
