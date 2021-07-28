# -*- coding: utf-8 -*-

import ovirtsdk4

from . import (
    clusters,
    data_centers,
    disks,
    storage_domains,
    hosts,
    networks,
    network_providers,
    pools,
    templates,
    vms,
    vnic_profiles,
    defaults,
    events,
    mac_pools
)


class OvirtLib(object):
    def __init__(
            self,
            host,
            password,
            username=defaults.ADMIN_USERNAME,
            ca_file=None,
            insecure=True,
            https=True,
            logger=None,
            debug=False
    ):

        self.host = host
        self.url = "{http}://{host}/ovirt-engine/api".format(
            http="https" if https else "http", host=host
        )
        self.username = username
        self.password = password
        self.ca_file = ca_file
        self.insecure = insecure
        self.logger = logger
        self.debug = debug

        self.ovirt_connection = self.connect()
        params = {"connection": self.ovirt_connection}

        self._hosts = hosts.Hosts(**params)
        self._vms = vms.Vms(**params)
        self._vnic_profiles = vnic_profiles.VnicProfiles(**params)
        self._clusters = clusters.Clusters(**params)
        self._data_centers = data_centers.DataCenters(**params)
        self._disks = disks.Disks(**params)
        self._storage_domains = storage_domains.StorageDomains(**params)
        self._networks = networks.Networks(**params)
        self._network_providers = network_providers.NetworkProvisers(**params)
        self._templates = templates.Templates(**params)
        self._pools = pools.Pools(**params)
        self._events = events.Events(**params)
        self._mac_pools = mac_pools.MacPools(**params)

    def connect(self):
        """
        Connects to the remote oVirt instance.
        """
        return ovirtsdk4.Connection(
            url=self.url,
            username=self.username,
            password=self.password,
            insecure=self.insecure,
            ca_file=self.ca_file,
            log=self.logger,
            debug=self.debug
        )

    def follow_link(self, obj):
        """
        Call to the SDK follow_link() method without any wrapping
        Follows the `href` attribute of given object, and retrieves the object

        Args:
            obj: SDK object that include href attribute

        Returns:
            ovirtsdk4.type.Struct: Any SDK object
        """
        return self.ovirt_connection.follow_link(obj=obj)

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
    def storage_domains(self):
        return self._storage_domains

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

    @property
    def mac_pools(self):
        return self._mac_pools
