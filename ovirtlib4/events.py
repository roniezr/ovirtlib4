# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Events(CollectionService):
    """
    Gives access to all Ovirt Events
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().events_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().event_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Event

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return EventEntity(connection=self.connection)


class EventEntity(CollectionEntity):
    """
    Put Event custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
