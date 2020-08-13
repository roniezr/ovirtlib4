# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .system_service import CollectionService, CollectionEntity


class DataCenters(CollectionService):
    """
    Gives access to all Ovirt Data Centers
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().data_centers_service()
        self.entity_service = self.service.data_center_service
        self.entity_type = types.DataCenter

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DadaCenterEntity(connection=self.connection)


class DadaCenterEntity(CollectionEntity):
    """
    Put Data-center custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
