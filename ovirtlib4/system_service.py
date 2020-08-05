# -*- coding: utf-8 -*-

import collections
import logging
import types

from .utils.sampler import APITimeout
from .utils.sampler import TimeoutingSampler

logger = logging.getLogger(__name__)


class RootService(object):
    """
    Hold the root oVirt connection

    Attributes:
        connection (ovirtsdk4.Connection): oVirt connection
    """
    def __init__(self, connection=None, follows=None):
        self._connection = connection
        self._follows = follows

    @property
    def connection(self):
        return self._connection

    @property
    def follows(self):
        """
        Add links to follow
        For more information about the 'follow' list() parameter please refer to the SDK documentation

        Returns:
            str: Links names separated with a comma,
                e.g.: links for networks "data_center,networklabels,vnicprofiles,permissions"
                    It will generate the following URI:
                    https://<fqdn>/ovirt-engine/api/networks?follow=data_center,networklabels,vnicprofiles,permissions

        """
        return self._follows

    @follows.setter
    def follows(self, follows):
        """ User can update the follows parameter """
        self._follows = follows

    def run_sampler(self, wait_for, func, wait_method="any", wait_timeout=5, wait_interval=1, *args, **kwargs):
        """
        Sample the list() method

        Args:
            wait_for (object): The algorithm to detect a successful method
                If 'bool': examine the list() returned value,
                    True - wait until list() will return a non-empty list
                    False - wait until list() will return an empty list
                If 'str': 'wait_for' will be examine for each field at the list,
                    wait until any or all fields are True (depend on 'wait_method')
                If 'function': Wait until given function return True
            wait_method (str): Can be "any" or "all" available only if given 'wait_for' value is string
                "all": all object at the list should match before exit the wait state
                "any": exit the wait state for first match
            wait_timeout (int): Timeout to wait for success in seconds
            wait_interval (int): Sleep interval between the samplers in seconds
            *args, **kwargs : Parameters to pass to the list() method

        Returns:
            list: List output is succeeded, None if timeout expired
        """
        sampler = TimeoutingSampler(
            timeout=wait_timeout,
            interval=wait_interval,
            func=func,
            *args,
            **kwargs
        )
        try:
            for sample in sampler:
                if sample:
                    result = self._process_sample(wait_for=wait_for, wait_method=wait_method, sample=sample)
                    if result:
                        return result

        except APITimeout:
            logger.error(
                f"Timeout '{wait_timeout}' expired while waiting for True value "
                f"of wait_for='{wait_for}' form object '{self.__class__}'"
            )
            return None

    def _process_sample(self, wait_for, wait_method, sample):
        """
        Handle a result sample according to the given 'wait_for' and 'wait_method'

        Args:
            wait_for (object): see run_sampler() docstring
            wait_method (str): see run_sampler() docstring
            sample (list): List of SDK entities, returned by get()

        Returns:
            list: If 'str' or 'bool' return the given sample if it match,
                if 'str' return the filtered list if it match,
                if no match return an empty list
        """
        if type(wait_for) == bool:
            if bool(sample) == wait_for:
                return sample

        if callable(wait_for):
            results = eval("wait_for(sample)")
            if results:
                return sample

        if type(wait_for) == str:
            results = []
            true_objects = []
            for obj in sample:
                result = eval(f"obj.{wait_for}")
                results.append(result)
                logger.debug(
                    f"Wait for True value of: '{wait_for}', for object name: '{obj.entity.name}', got value: {result}"
                )
                if result:
                    true_objects.append(obj)

            if eval(f"{wait_method}(results)"):
                return true_objects

        return []

    def get(self, func, wait_for=None, *args, **kwargs):
        """
        Call to list()

        Args:
            wait_for (object): See run_sampler() docstring

        Returns:
            list: List of CollectionEntity objects
        """
        if 'follow' not in kwargs.keys() and self.follows:
            kwargs['follow'] = self.follows

        if wait_for is not None:
            return self.run_sampler(func=func, wait_for=wait_for, *args, **kwargs)

        return func(*args, **kwargs)


class CollectionService(RootService):
    """
    Abstract class, represent an oVirt collection
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._service = NotImplementedError
        self._entity_service = NotImplementedError
        self._entity_type = NotImplementedError

    @property
    def service(self):
        """ Return the main collection service e.g.: vms_service(), hosts_service() """
        return self._service

    @service.setter
    def service(self, service):
        """ The collection service must be set by the inherit class """
        self._service = service

    @property
    def entity_service(self):
        """ Return the service of an individual entity of the collection """
        return self._entity_service

    @entity_service.setter
    def entity_service(self, entity_service):
        """ The _entity_service must be set by the inherit class """
        self._entity_service = entity_service

    @property
    def entity_type(self):
        """
        Abstract method, return an individual entity type of the collection
        The return type is a class from: ovirtsdk4.types

        The type is required to add or modify a collection entity
        user can use ovirtsdk4.types or get the Struct type by calling this method
        """
        return self.entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """ The entity type must be set by the inherit class """
        self._entity_type = entity_type

    def get_entity_by_id(self, id):
        """
        Return a CollectionEntity class based on given ID
        """
        collection_entity = self._get_collection_entity()
        collection_entity.entity = self.entity_service(id=id).get()
        collection_entity.service = self.entity_service(id=id)

        return collection_entity

    def _create_collection_entity(self, entity):
        """
        Return a wrapper collection entity that include the entity and its service

        Args:
            entity (ovirtsdk4.types): Any SDK type object
        """
        collection_entity = self._get_collection_entity()

        collection_entity.entity = entity
        collection_entity.service = self.entity_service(id=entity.id)

        return collection_entity

    def _get_collection_entity(self):
        """
        Return a CollectionEntity class
        An inherit class can overwrite this method to return its own CollectionEntity class
        """
        return CollectionEntity(connection=self.connection)

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Call to list()

        Returns:
            list: List of CollectionEntity objects
        """
        return super().get(func=self.list, *args, **kwargs)

    def list(self, *args, **kwargs):
        """
        Change the list() method of a collection service to return our CollectionEntity object.
        Our CollectionEntity class will include the entity Type and its Service while the API
        service list() method return only the entities Type
        All the main list() API function abilities are kept and supported
        """
        entities = []
        if isinstance(self.service, types.MethodType):
            return_entities = self.service().list(*args, **kwargs)
        else:
            return_entities = self.service.list(*args, **kwargs)
        for entity in return_entities:
            entities.append(self._create_collection_entity(entity=entity))
        return entities

    def get_names(self, *args, **kwargs):
        """
        Return names of all collection entities

        Returns:
            list: Entities names
        """
        names = []
        for entity in self.list(*args, **kwargs):
            names.append(entity.entity.name)
        return names


class CollectionEntity(RootService):
    """
    Represent an ovirt entity (e.g.: vm, host)
    The class hold the entity 'type' and 'service' e.g.: type.Vm(),  vm_service()

    Inherit this class to add custom individual Entity methods

    Attributes:
        entity (ovirtsdk4.Struct): The individual entity of a collection
        service (ovirtsdk4.Service): The service of the individual entity of a collection
    """
    def __init__(self, entity=None, service=None, *args, **kwargs):
        RootService.__init__(self, *args, **kwargs)
        self._entity = entity
        self._service = service

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._entity = super().get(func=self.service.get, *args, **kwargs)
        return self

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity):
        self._entity = entity

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def follow_link(self, link, collection_service=None):
        """
        Follow a link of an Entity and retrieve its attached entities

        Args:
            link (ovirtsdk4.types): Entity link to retrieve
            collection_service (CollectionService): The collection-service that represent the retrieves link entity

        Returns:
            list (CollectionEntity): Retrieved entities list,
                if collection_service is ot given, then CollectionEntity.service will be None
        """
        entities = self.connection.follow_link(obj=link)
        if not isinstance(entities, collections.Iterable):
            entities = [entities]

        collection_entities = []
        collection_entity = collection_service._get_collection_entity() if collection_service else CollectionEntity()
        for entity in entities:
            collection_entity.entity = entity
            collection_entity.service = (
                collection_service.entity_service(id=entity.id)
                if collection_service
                else collection_service
            )
            collection_entities.append(collection_entity)
        return collection_entities
