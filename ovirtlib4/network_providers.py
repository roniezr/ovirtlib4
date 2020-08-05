# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class NetworkProvisers(CollectionService):
    """
    Gives access to all oVirt Network Providers
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().openstack_network_providers_service()
        self.entity_service = self.service.provider_service
        self.entity_type = types.ExternalNetworkProviderConfiguration
        self.follows = "networks,certificates"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return NetworkProvider()


class NetworkProvider(CollectionEntity):
    """
    Put NetworkProvider custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
