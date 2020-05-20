# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Networks(CollectionService):
    """
    Gives access to all oVirt Networks
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().networks_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().network_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Network

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return NetworkEntity(connection=self.connection)


class NetworkEntity(CollectionEntity):
    """
    Put Network custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
