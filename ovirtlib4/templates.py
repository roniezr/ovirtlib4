# -*- coding: utf-8 -*-

import ovirtsdk4.types as types

from .clusters import ClusterAssociated
from .system_service import CollectionService, CollectionEntity


class Templates(CollectionService):
    """
    Gives access to all Ovirt Templates
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().templates_service()
        self.entity_service = self.service.template_service
        self.entity_type = types.Template

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return TemplateEntity(connection=self.connection)


class TemplateEntity(CollectionEntity, ClusterAssociated):
    """
    Put Template custom functions here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
