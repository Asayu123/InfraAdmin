from django.db import models
from django.core import validators

# Create your models here.


class Environment(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name


class DataCenter(models.Model):
    #POS_CHOICES = (('front', 'フロント'), ('back', 'バック'), ('kibi', '機微'))
    name = models.CharField(max_length=32, primary_key=True)
    environment_name = models.ForeignKey('ServerAdmin.Environment', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class VCenterCluster(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    HA_available = models.BooleanField()
    DataCenter_name = models.ForeignKey('DataCenter', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Rack(models.Model):
    name = models.CharField(max_length=64, primary_key=True)  # strings
    console_name = models.CharField(max_length=64, unique=True)  # string, match to node number,console number
    environment_name = models.ForeignKey('ServerAdmin.Environment', to_field='name', on_delete=models.PROTECT)
    num_of_unit = models.IntegerField(default=32)

    def __str__(self):
        return self.name


class HypervisorUsage(models.Model):# Like "DB","SPARE"
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name


class PhysicalServer(models.Model):
    serial = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    product_name = models.CharField(max_length=64)
    usage = models.CharField(max_length=128)
    environment_name = models.ForeignKey('ServerAdmin.Environment', to_field='name', on_delete=models.PROTECT)

    #following info is used when visualizing server layout
    rack_name = models.ForeignKey('ServerAdmin.Rack', to_field='name',on_delete=models.PROTECT)
    rack_unit_start = models.PositiveIntegerField()
    rack_unit_end = models.PositiveIntegerField()

    #following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()


class HypervisorHost(models.Model):
    # management data
    name = models.CharField(max_length=64, primary_key=True)
    reserved = models.BooleanField(default=False)

    # specification
    cpu_core_num = models.PositiveIntegerField()
    memory_capacity_GB = models.PositiveIntegerField() #GigaByte
    hdd_capacity_GB = models.PositiveIntegerField() #GigaByte

    # following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    # reference
    vCenterCluster_name = models.ForeignKey('ServerAdmin.VCenterCluster', to_field='name', on_delete=models.PROTECT)
    physicalserver_name = models.OneToOneField('ServerAdmin.PhysicalServer', to_field='name', on_delete=models.PROTECT)
    hypervisorusage_name = models.ForeignKey('ServerAdmin.HypervisorUsage', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Datastore(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField()  # Unit is GigaByte

    def __str__(self):
        return self.name


class NFS_Storage(models.Model): # Use this table to define NFS Datastore's network Path.
    datastore_name = models.ForeignKey('ServerAdmin.Datastore', to_field='name', primary_key=True, on_delete=models.PROTECT)
    ipaddr = models.IPAddressField()
    path = models.CharField(max_length=128)

    def __str__(self):
        return self.datastore_name


class VLAN(models.Model):# Define Relationship between VLANID , Usage , IPRange
    id = models.IntegerField(primary_key=True, validators=[validators.MinValueValidator(0),validators.MaxValueValidator(4096)])
    usage = models.CharField(max_length=256)
    nwaddr = models.IPAddressField()
    prefix = models.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(32)])


class VirtualMachine(models.Model):
    # id = models.AutoField(primary_key=True) is defined Automatically, implicitly
    # HDD and NIC information is stored in another class (i.e:List / Table)
    name = models.CharField(max_length=64, primary_key=True)
    usage = models.CharField(max_length=256)
    os = models.CharField(max_length=64)
    cpu = models.PositiveIntegerField()
    memory_GB = models.PositiveIntegerField()  # Unit is GigaByte
    HA_required = models.BooleanField()
    note = models.CharField(max_length=1024)

    # following attribute is linked to another table.

    hypervisor_name = models.ForeignKey('ServerAdmin.HypervisorHost', to_field='name', on_delete=models.PROTECT)
    vminstalledsoftware_name = models.ManyToManyField('ServerAdmin.VmInstalledSoftware')
    vmserverspectest_name = models.ManyToManyField('ServerAdmin.VmServerSpecTest')
    vmchefrecipe_name = models.ManyToManyField('ServerAdmin.VmChefRecipe')

    #following attribute is for logging.
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return self.name


class VmAttachedVirtualHDD(models.Model):
    id = models.AutoField(primary_key=True)
    virtualmachine_name = models.ForeignKey('ServerAdmin.VirtualMachine', to_field='name',on_delete=models.CASCADE)
    mount_point = models.CharField(max_length=256)
    capacity_GB = models.PositiveIntegerField()  # Unit is GigaByte will be Stored
    datastore_name = models.ForeignKey('ServerAdmin.Datastore', to_field='name', on_delete=models.PROTECT)

    def __str__(self):
        return self.id


class VmAttachedNIC(models.Model):
    id = models.AutoField(primary_key=True)
    virtualmachine_name = models.ForeignKey('ServerAdmin.VirtualMachine', to_field='name', on_delete=models.CASCADE)  # vmID will be "id" that has been created in class "VirtualMachine"
    vLAN_id = models.ForeignKey('ServerAdmin.VLAN', to_field='id',on_delete=models.PROTECT)
    IP_Address = models.GenericIPAddressField()

    def __str__(self):
        return self.id


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
