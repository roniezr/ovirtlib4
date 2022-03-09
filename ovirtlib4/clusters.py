# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from . import mac_pools as mac_pool_collection, networks
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
        To update new mac-pool to the cluster use the ovirtlib.cluster.service.update()
        To add new mac-pool use the ovirtlib.mac_pools.service.add()
        """
        return self.follow_link(
            link=self.entity.mac_pool,
            collection_service=mac_pool_collection.MacPools(connection=self.connection)
        )

    def get_management_network(self):
        """
        Gets the management network of the cluster

        Returns:
            ovirtib4.NetworkEntity: ovirtLib4 NetworkEntity object
        """
        for network in self.get(follow="networks").entity.networks:
            if types.NetworkUsage.MANAGEMENT in network.usages:
                return networks.Networks(self.connection).get_entity_by_id(id=network.id)
        return None


class ClusterAssociated(object):
    """
    Represents an ovirtlib entity associated with a cluster
    """
    @property
    def get_cluster(self):
        """
        Gets the cluster the entity is associated with

        Returns:
             ClusterAssociated: ovirtlib4 ClusterEntity object if entity has a cluster ID, None otherwise
        """
        try:
            cluster_id = self.entity.cluster.id
        except AttributeError:
            return None
        return Clusters(connection=self.connection).get_entity_by_id(id=cluster_id)
