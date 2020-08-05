# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class DataCenters(CollectionService):
    """
    Gives access to all Ovirt Data Centers
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().data_centers_service()
        self.entity_service = self.service.data_center_service
        self.entity_type = types.DataCenter
        self.follows = "storagedomains,permissions,networks,clusters,quotas,qoss,iscsibonds"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DadaCenterEntity(connection=self.connection)


class DadaCenterEntity(CollectionEntity):
    """
    Put Data-center custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
