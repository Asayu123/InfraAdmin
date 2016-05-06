# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 09:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataCenter',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Datastore',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=256)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='HypervisorHost',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('reserved', models.BooleanField(default=False)),
                ('cpu_core_num', models.PositiveIntegerField()),
                ('memory_capacity_GB', models.PositiveIntegerField()),
                ('hdd_capacity_GB', models.PositiveIntegerField()),
                ('creation_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='HypervisorUsage',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalServer',
            fields=[
                ('serial', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('product_name', models.CharField(max_length=64)),
                ('usage', models.CharField(max_length=128)),
                ('rack_unit_start', models.PositiveIntegerField()),
                ('rack_unit_end', models.PositiveIntegerField()),
                ('creation_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('environment_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.Environment')),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('console_name', models.CharField(max_length=64, unique=True)),
                ('num_of_unit', models.IntegerField(default=32)),
                ('environment_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.Environment')),
            ],
        ),
        migrations.CreateModel(
            name='VCenterCluster',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('HA_available', models.BooleanField()),
                ('DataCenter_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.DataCenter')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('usage', models.CharField(max_length=256)),
                ('os', models.CharField(max_length=64)),
                ('cpu', models.PositiveIntegerField()),
                ('memory_GB', models.PositiveIntegerField()),
                ('HA_required', models.BooleanField()),
                ('note', models.CharField(max_length=1024)),
                ('creation_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('hypervisorhost_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.HypervisorHost')),
            ],
        ),
        migrations.CreateModel(
            name='VLAN',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4096)])),
                ('usage', models.CharField(max_length=256)),
                ('nwaddr', models.GenericIPAddressField()),
                ('prefix', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32)])),
            ],
        ),
        migrations.CreateModel(
            name='VmAttachedVirtualHDD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mount_point', models.CharField(max_length=256)),
                ('capacity_GB', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VmAttachedVirtualNIC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('IP_Address', models.GenericIPAddressField()),
                ('vLAN_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.VLAN')),
                ('virtualmachine_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServerAdmin.VirtualMachine')),
            ],
        ),
        migrations.CreateModel(
            name='VmChefRecipe',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='VmInstalledSoftware',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='VmServerSpecTest',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='NFS_Storage',
            fields=[
                ('datastore_name', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='ServerAdmin.Datastore')),
                ('ipaddr', models.GenericIPAddressField()),
                ('path', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='vmattachedvirtualhdd',
            name='datastore_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.Datastore'),
        ),
        migrations.AddField(
            model_name='vmattachedvirtualhdd',
            name='virtualmachine_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServerAdmin.VirtualMachine'),
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='vmchefrecipe_name',
            field=models.ManyToManyField(to='ServerAdmin.VmChefRecipe'),
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='vminstalledsoftware_name',
            field=models.ManyToManyField(to='ServerAdmin.VmInstalledSoftware'),
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='vmserverspectest_name',
            field=models.ManyToManyField(to='ServerAdmin.VmServerSpecTest'),
        ),
        migrations.AddField(
            model_name='physicalserver',
            name='rack_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.Rack'),
        ),
        migrations.AddField(
            model_name='hypervisorhost',
            name='hypervisorusage_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.HypervisorUsage'),
        ),
        migrations.AddField(
            model_name='hypervisorhost',
            name='physicalserver_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.PhysicalServer', to_field='name'),
        ),
        migrations.AddField(
            model_name='hypervisorhost',
            name='vCenterCluster_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.VCenterCluster'),
        ),
        migrations.AddField(
            model_name='datacenter',
            name='environment_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ServerAdmin.Environment'),
        ),
    ]
