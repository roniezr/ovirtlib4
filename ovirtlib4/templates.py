# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Templates(CollectionService):
    """
    Gives access to all Ovirt Templates
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().templates_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().template_service(id=id)

    def get_entity_type(self):
        """ Overwrite abstract parent method """
        return types.Template

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return TemplateEntity(connection=self.connection)


class TemplateEntity(CollectionEntity):
    """
    Put Template custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
