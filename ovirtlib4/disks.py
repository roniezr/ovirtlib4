# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Disks(CollectionService):
    """
    Gives access to all Ovirt Disks
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().disks_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().disk_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Disk

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DiskEntity(connection=self.connection)


class DiskEntity(CollectionEntity):
    """
    Put Disk custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
