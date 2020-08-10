# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .system_service import CollectionService, CollectionEntity


class VnicProfiles(CollectionService):
    """
    Gives access to all Ovirt VnicProfiles
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vnic_profiles_service()
        self.entity_service = self.service.profile_service
        self.entity_type = types.VnicProfile

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VnicProfileEntity(connection=self.connection)


class VnicProfileEntity(CollectionEntity):
    """
    Put VnicProfile custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
