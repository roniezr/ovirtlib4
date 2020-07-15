# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Hosts(CollectionService):
    """
    Gives access to all Ovirt Hosts
    """
    @property
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().hosts_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service.host_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Host

    def get_spm_host(self):
        for host in self.list():
            if host.entity.spm.status.value != 'none':
                return host
        return None

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostEntity(connection=self.connection)


class HostEntity(CollectionEntity):
    """
    Put Host custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

    @property
    def nics(self):
        """Return HostNics class"""
        return HostNics(connection=self.service)

    @property
    def statistics(self):
        """Return HostStatistics class"""
        return HostStatistics(connection=self.service)


class HostNics(CollectionService):
    """
    Gives access to all Host NICs
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.nics_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().nic_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.HostNic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostNic(connection=self.connection)


class HostNic(CollectionEntity):
    """
    Put HostNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)


class HostStatistics(CollectionService):
    """
    Gives access to all Host NICs
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.statistics_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().statistic_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Statistic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostStatistic(connection=self.connection)


class HostStatistic(CollectionEntity):
    """
    Put HostNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
