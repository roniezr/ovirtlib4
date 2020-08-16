# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .system_service import CollectionService, CollectionEntity


class MacPools(CollectionService):
    """
    Gives access to all Ovirt MAC Pools
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().mac_pools_service()
        self.entity_service = self.service.mac_pool_service
        self.entity_type = types.MacPool

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return MacPoolEntity(connection=self.connection)


class MacPoolEntity(CollectionEntity):
    """
    Put MacPool custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
