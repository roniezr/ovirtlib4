# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Pools(CollectionService):
    """
    Gives access to all Ovirt VM Pools
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().vm_pools_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().pool_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.VmPool

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return PoolEntity(connection=self.connection)


class PoolEntity(CollectionEntity):
    """
    Put Pool custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
