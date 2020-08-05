# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Disks(CollectionService):
    """
    Gives access to all Ovirt Disks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().disks_service()
        self.entity_service = self.service.disk_service
        self.entity_type = types.Disk
        self.follows = "permissions,statistics,disk_profile,quota"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DiskEntity(connection=self.connection)


class DiskEntity(CollectionEntity):
    """
    Put Disk custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
