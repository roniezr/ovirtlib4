# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Pools(CollectionService):
    """
    Gives access to all Ovirt VM Pools
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vm_pools_service()
        self.entity_service = self.service.pool_service
        self.entity_type = types.VmPool

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return PoolEntity(connection=self.connection)


class PoolEntity(CollectionEntity):
    """
    Put Pool custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
