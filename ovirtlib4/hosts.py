# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Hosts(CollectionService):
    """
    Gives access to all Ovirt Hosts
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().hosts_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().host_service(id=id)

    def get_entity_type(self):
        """ Overwrite abstract parent method """
        return types.Host

    def get_spm_host(self):
        for host in self.list():
            if host.entity.spm.status.value != 'none':
                return host
        return None

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostEntity(connection=self.connection)


class HostEntity(CollectionEntity):
    """
    Put Host custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
