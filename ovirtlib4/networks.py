# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Networks(CollectionService):
    """
    Gives access to all oVirt Networks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().networks_service()
        self.entity_service = self.service.network_service
        self.entity_type = types.Network
        self.follows = "permissions,vnicprofiles,networklabels,data_center"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return NetworkEntity(connection=self.connection)


class NetworkEntity(CollectionEntity):
    """
    Put Network custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
