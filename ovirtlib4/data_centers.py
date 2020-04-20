# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class DataCenters(CollectionService):
    """
    Gives access to all Ovirt Data Centers
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().data_centers_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().data_center_service(id=id)

    def get_entity_type(self):
        """ Overwrite abstract parent method """
        return types.DataCenter

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DadaCenterEntity(connection=self.connection)


class DadaCenterEntity(CollectionEntity):
    """
    Put Data-center custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
