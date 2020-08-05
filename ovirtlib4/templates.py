# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Templates(CollectionService):
    """
    Gives access to all Ovirt Templates
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().templates_service()
        self.entity_service = self.service.template_service
        self.entity_type = types.Template
        self.follows = "permissions,tags,diskattachments,graphicsconsoles,cdroms,nics,watchdogs"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return TemplateEntity(connection=self.connection)


class TemplateEntity(CollectionEntity):
    """
    Put Template custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
