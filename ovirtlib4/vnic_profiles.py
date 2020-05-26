# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class VnicProfiles(CollectionService):
    """
    Gives access to all Ovirt VnicProfiles
    """
    @property
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().vnic_profiles_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service.profile_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.VnicProfile

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VnicProfileEntity(connection=self.connection)


class VnicProfileEntity(CollectionEntity):
    """
    Put VnicProfile custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
