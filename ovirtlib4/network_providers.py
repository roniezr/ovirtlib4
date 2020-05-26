# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class NetworkProvisers(CollectionService):
    """
    Gives access to all oVirt Network Providers
    """
    @property
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().openstack_network_providers_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service.provider_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.ExternalNetworkProviderConfiguration

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return NetworkProvider()


class NetworkProvider(CollectionEntity):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
