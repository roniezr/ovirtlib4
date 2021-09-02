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

    @property
    def storage_domains(self):
        return DataCenterStorageDomains(connection=self.service)


class DataCenterStorageDomains(CollectionService):
    """
    Gives access to all Storage Domains belonging to the Data Center
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.storage_domains_service()
        self.entity_service = self.service.storage_domain_service
        self.entity_type = types.StorageDomain

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DataCenterStorageDomain(connection=self.connection)


class DataCenterStorageDomain(CollectionEntity):
    """
    Put DataCenterStorageDomain custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
