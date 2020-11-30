# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from . import defaults, hosts
from .system_service import CollectionService, CollectionEntity


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


class VmEntity(CollectionEntity):
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
