# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Domains(CollectionService):
    """
    Gives access to all Ovirt Domains
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().storage_domains_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().storage_domain_service(id=id)

    def get_entity_type(self):
        """ Overwrite abstract parent method """
        return types.Domain

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return DomainEntity(connection=self.connection)


class DomainEntity(CollectionEntity):
    """
    Put Domain custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
