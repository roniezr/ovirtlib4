# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Clusters(CollectionService):
    """
    Gives access to all Ovirt Clusters
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().clusters_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().cluster_service(id=id)

    def get_entity_type(self):
        """ Overwrite abstract parent method """
        return types.Cluster

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return ClusterEntity(connection=self.connection)


class ClusterEntity(CollectionEntity):
    """
    Put Disk custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
