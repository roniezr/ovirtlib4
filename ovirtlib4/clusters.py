# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Clusters(CollectionService):
    """
    Gives access to all Ovirt Clusters
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().clusters_service()
        self.entity_service = self.service.cluster_service
        self.entity_type = types.Cluster
        self.follows = (
            "permissions,"
            "networkfilters,"
            "networks,"
            "affinitygroups,"
            "glusterhooks,"
            "glustervolumes,"
            "enabledfeatures,"
            "cpuprofiles"
        )

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return ClusterEntity(connection=self.connection)


class ClusterEntity(CollectionEntity):
    """
    Put Cluster custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
