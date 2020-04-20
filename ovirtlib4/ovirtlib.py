# -*- coding: utf-8 -*-

import ovirtsdk4
# from . import(
from art.rhevm_api.ovirtlib4 import (
    clusters,
    data_centers,
    disks,
    domains,
    hosts,
    networks,
    network_providers,
    pools,
    templates,
    vms,
    vnic_profiles,
    defaults,
    events
)


class OvirtLib(object):
    def __init__(self, host, password, username=defaults.ADMIN_USERNAME, ca_file=None, insecure=True, https=True):

        self.host = host
        self.url = "{http}://{host}/ovirt-engine/api".format(
            http="https" if https else "http", host=host
        )
        self.username = username
        self.password = password
        self.ca_file = ca_file
        self.insecure = insecure

        self.ovirt_connection = self.connect()

        self._hosts = hosts.Hosts(connection=self.ovirt_connection)
        self._vms = vms.Vms(connection=self.ovirt_connection)
        self._vnic_profiles = vnic_profiles.VnicProfiles(connection=self.ovirt_connection)
        self._clusters = clusters.Clusters(connection=self.ovirt_connection)
        self._data_centers = data_centers.DataCenters(connection=self.ovirt_connection)
        self._disks = disks.Disks(connection=self.ovirt_connection)
        self._domains = domains.Domains(connection=self.ovirt_connection)
        self._networks = networks.Networks(connection=self.ovirt_connection)
        self._network_providers = network_providers.NetworkProvisers(connection=self.ovirt_connection)
        self._templates = templates.Templates(connection=self.ovirt_connection)
        self._pools = pools.Pools(connection=self.ovirt_connection)
        self._events = events.Events(connection=self.ovirt_connection)

    def connect(self, *args, **kwargs):
        """ Made the HTTP connection to remote Engine """
        return ovirtsdk4.Connection(
            url=self.url,
            username=self.username,
            password=self.password,
            insecure=self.insecure,
            ca_file=self.ca_file,
            *args, **kwargs
        )

    @property
    def hosts(self):
        return self._hosts

    @property
    def vms(self):
        return self._vms

    @property
    def vnic_profiles(self):
        return self._vnic_profiles

    @property
    def clusters(self):
        return self._clusters

    @property
    def data_centers(self):
        return self._data_centers

    @property
    def disks(self):
        return self._disks

    @property
    def domains(self):
        return self._domains

    @property
    def networks(self):
        return self._networks

    @property
    def network_providers(self):
        return self._network_providers

    @property
    def pools(self):
        return self._pools

    @property
    def templates(self):
        return self._templates

    @property
    def events(self):
        return self._events
