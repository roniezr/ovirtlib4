# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .system_service import CollectionService, CollectionEntity


class Clusters(CollectionService):
    """
    Gives access to all Ovirt Clusters
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().clusters_service()
        self.entity_service = self.service.cluster_service
        self.entity_type = types.Cluster

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return ClusterEntity(connection=self.connection)


class ClusterEntity(CollectionEntity):
    """
    Put Cluster custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
