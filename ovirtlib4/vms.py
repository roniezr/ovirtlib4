# -*- coding: utf-8 -*-

import ipaddress
import ovirtsdk4.types as types

from . import defaults, hosts, vnic_profiles
from .system_service import CollectionService, CollectionEntity, ClusterAssociated


class Vms(CollectionService):
    """
    Gives access to all Ovirt VMs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vms_service()
        self.entity_service = self.service.vm_service
        self.entity_type = types.Vm

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmEntity(connection=self.connection)

    def get_vms(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return all VMs beside the HostedEngine VM """
        return self.list(search="name!={name}".format(name=he_name))

    def get_hosted_engine_vm(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return the hosted-engine VM: (VmEntity) """
        vms = self.list(search="name={name}".format(name=he_name))
        if vms:
            return vms[0]
        return None

    def get_hosted_engine_host(self):
        """
        Return the host Entity of the HostedEngine VM, or None if not found
        """
        vm = self.get_hosted_engine_vm()
        if vm:
            host_id = vm.entity.host.id
            if host_id:
                return hosts.Hosts(self.connection).get_entity_by_id(id=host_id)
        return None


class VmEntity(CollectionEntity, ClusterAssociated):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

    @property
    def nics(self):
        return VmNics(connection=self.service)

    @property
    def disks(self):
        return VmDisks(connection=self.service)

    @property
    def backups(self):
        return VmBackups(connection=self.service)

    @property
    def reported_devices(self):
        return VmReportedDevices(connection=self.service)

    @property
    def snapshots(self):
        return VmSnapshots(connection=self.service)

    def start_and_wait(self, state=types.VmStatus.UP.value, wait_timeout=defaults.VM_START_TIMEOUT, *args, **kwargs):
        """
        Start VM and wait for it to start

        Args:
            state (str): VM state to wait for (default 'up')

        Returns:
             VmEntity: The updated VM object if start VM succeeded, None otherwise
        """
        if self.get().entity.status.value == types.VmStatus.DOWN.value:
            self.service.start()
        vm = self.get(
            wait_for=f"entity.status.value == '{state}'",
            wait_timeout=wait_timeout,
            *args,
            **kwargs
        )
        return vm[0] if vm else None

    def stop_and_wait(self, state=types.VmStatus.DOWN.value, *args, **kwargs):
        """
        Stop VM and wait for it to stop

        Args:
            state (str): VM state to wait for (default 'down')

        Returns:
             VmEntity: The updated VM object if stop VM succeeded, None otherwise
        """
        self.service.stop()
        vm = self.get(wait_for=f"entity.status.value == '{state}'", *args, **kwargs)
        return vm[0] if vm else None

    def get_management_nic(self):
        """
        Gets the management vNIC of the VM

        Args:
            mng_network (str): Management network name

        Returns:
            VmNic: ovirtlib VmNic object if vNIC was found, None otherwise
        """
        cluster = self.get_cluster
        if cluster:
            mng_network = cluster.get_management_network()
            for nic in self.nics():
                if nic.get_vnic_profile().entity.network.id == mng_network.entity.id:
                    return nic
        return None


class VmNics(CollectionService):
    """
    Gives access to all VM NICs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.nics_service()
        self.entity_service = self.service.nic_service
        self.entity_type = types.Nic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmNic(connection=self.connection)


class VmNic(CollectionEntity):
    """
    Put VmNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

    def get_vnic_profile(self):
        """
        Gets the vNIC profile

        Returns:
            ovirtlib4.vnic_profile.VnicProfileEntity: ovirlib4 VnicProfileEntity object
        """
        return vnic_profiles.VnicProfiles(connection=self.root_connection).get_entity_by_id(
            id=self.entity.vnic_profile.id
        )

    def get_ips(self, ip_version=ipaddress.IPv4Address):
        """
        Get VM IPs

        Args:
            ip_version (ipaddress): IP version to retrieve, default v4

        Returns:
            list (str): List of IPs
        """
        reported_devices = self.get(follow="reported_devices").entity.reported_devices
        if reported_devices:
            for reported_device in reported_devices:
                if reported_device and hasattr(reported_device, 'ips'):
                    return [
                        ip.address for ip in reported_device.ips
                        if type(ipaddress.ip_address(ip.address)) == ip_version
                    ]
        return []


class VmDisks(CollectionService):
    """
    Gives access to all VM attached disks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.disk_attachments_service()
        self.entity_service = self.service.attachment_service
        self.entity_type = types.DiskAttachment

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmDisk(connection=self.connection)


class VmDisk(CollectionEntity):
    """
    Put VmDisk custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)


class VmBackups(CollectionService):
    """
    Gives access to all VM Backups
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.backups_service()
        self.entity_service = self.service.backup_service
        self.entity_type = types.Backup

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmBackup(connection=self.connection)


class VmBackup(CollectionEntity):
    """
    Put VmBackup custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)


class VmReportedDevices(CollectionService):
    """
    Gives access to all VM Reported Devices
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.reported_devices_service()
        self.entity_service = self.service.reported_device_service
        self.entity_type = types.ReportedDevice

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmReportedDevice(connection=self.connection)


class VmReportedDevice(CollectionEntity):
    """
    Put VmReportedDevice custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)


class VmSnapshots(CollectionService):
    """
    Gives access to all VM Snapshots
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.snapshots_service()
        self.entity_service = self.service.snapshot_service
        self.entity_type = types.Snapshot

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmSnapshot(connection=self.connection)


class VmSnapshot(CollectionEntity):
    """
    Put VmSnapshot custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
