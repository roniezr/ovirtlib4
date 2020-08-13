# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .system_service import CollectionService, CollectionEntity


class StorageDomains(CollectionService):
    """
    Gives access to all Ovirt Storage Domains
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().storage_domains_service()
        self.entity_service = self.service.storage_domain_service
        self.entity_type = types.StorageDomain

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return StorageDomainEntity(connection=self.connection)


class StorageDomainEntity(CollectionEntity):
    """
    Put Storage Domain custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
