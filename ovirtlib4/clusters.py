# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from . import mac_pools as mac_pool_collection
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

    def mac_pools(self):
        """
        Return list of MAC-pools assign to the cluster

        This class returns the entity and service of the individual mac-pool allocated to the cluster
        To update new mac-pool to the cluster use the ovirtlib4.cluster.service.update()
        To add new mac-pool use the ovirtlib4.mac_pools.service.add()
        """
        return self.follow_link(
            link=self.entity.mac_pool,
            collection_service=mac_pool_collection.MacPools(connection=self.connection)
        )
