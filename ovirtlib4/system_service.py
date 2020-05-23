# -*- coding: utf-8 -*-


class RootService(object):
    """
    Hold the root oVirt connection

    Attributes:
        connection (ovirtsdk4.Connection): oVirt connection
    """
    def __init__(self, connection=None):
        self._connection = connection

    @property
    def connection(self):
        return self._connection


class CollectionService(RootService):
    """
    Abstract class, represent an oVirt collection
    """
    def service(self):
        """ Return the main collection service e.g.: vms_service(), hosts_service() """
        return NotImplementedError

    def _entity_service(self, id):
        """
        Return the service of an individual entity of the collection

        Args:
            id (str): Entity ID
        """
        return NotImplementedError

    def entity_type(self):
        """
        Abstract method, return an individual entity type of the collection
        The return type is a class from: ovirtsdk4.types

        The type is required to add or modify a collection entity
        user can use ovirtsdk4.types or get the Struct type by calling this method
        """
        return NotImplementedError

    def get_entity_by_id(self, id):
        """
        Return an entity Type of the the collection
        The return type is a class from: ovirtsdk4.types
        """
        return self._entity_service(id=id).get()

    def _get_collection_entity(self):
        """
        Return a CollectionEntity class
        An inherit class can overwrite this method to return its own CollectionEntity class
        """
        return CollectionEntity(connection=self.connection)

    def get(self, *args, **kwargs):
        """ Same as list() """
        return self.list(*args, **kwargs)

    def list(self, *args, **kwargs):
        """
        Change the list() method of a collection service to return our CollectionEntity object.
        Our CollectionEntity class will include the entity Type and its Service while the API
        service list() method return only the entities Type
        All the main list() API function abilities are kept and supported
        """
        entities = []

        for entity in self.service().list(*args, **kwargs):
            collection_entity = self._get_collection_entity()
            collection_entity.entity = entity
            collection_entity.service = self._entity_service(id=entity.id)
            entities.append(collection_entity)
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

    def get(self):
        self._entity = self.service.get()
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

        collection_entities = []
        for entity in entities:
            collection_entities.append(
                CollectionEntity(
                    entity=entity,
                    service=(
                        collection_service._entity_service(id=entity.id)
                        if collection_service else collection_service
                    )
                )
            )
        return collection_entities
