# -*- coding: utf-8 -*-

import logging

import ovirtsdk4.types as types

from .clusters import ClusterAssociated
from .system_service import CollectionService, CollectionEntity

logger = logging.getLogger(__name__)


class Hosts(CollectionService):
    """
    Gives access to all Ovirt Hosts
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().hosts_service()
        self.entity_service = self.service.host_service
        self.entity_type = types.Host

    def get_spm_host(self):
        for host in self.list():
            if host.entity.spm.status.value != 'none':
                return host
        return None

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostEntity(connection=self.connection)


class HostEntity(CollectionEntity, ClusterAssociated):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.nics_service()
        self.entity_service = self.service.nic_service
        self.entity_type = types.HostNic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostNicEntity(connection=self.connection)


class HostNicEntity(CollectionEntity):
    """
    Put HostNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)


class HostStatistics(CollectionService):
    """
    Gives access to all Host NICs
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.statistics_service()
        self.entity_service = self.service.statistic_service
        self.entity_type = types.Statistic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return HostStatisticEntity(connection=self.connection)

    def verify_statistics_value(self, statistics, expected_values):
        """
        Verify if given statistics values are as expected

        Args:
            statistics (ovirtlib4.hosts.HostStatistics): List of host statistics
            check_statistics (list): List of tuples when each tuple includes (statistics name, expression, value)

        Example:
            expected_values = {
                "cpu.current.user": "==0" ,
                "cpu.current.system": ">100",
            }

        Returns:
            bool: True if all statistics values are as expected, False otherwise
        """
        found_statistics = 0

        for statistic in statistics:
            if statistic.entity.name in expected_values.keys():
                found_statistics += 1
                for value in statistic.entity.values:
                    logger.debug(f"Verify {statistic.entity.name}={value.datum}")
                    if value.datum not in [None, ""] and not eval(
                        f"float(value.datum) {expected_values[statistic.entity.name]}"
                    ):
                        return False
        return found_statistics == len(expected_values)


class HostStatisticEntity(CollectionEntity):
    """
    Put HostStatistic custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
