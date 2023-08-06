# -*- coding: utf-8 -*-

from plone import schema
from plone.app.z3cform.widget import SingleCheckBoxBoolFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface, implementer, provider

from collective.excludefromcollection import _


class IExcludeFromCollectionMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IExcludeFromCollection(model.Schema):
    """ """

    model.fieldset(
        'settings',
        label=u'Settings',
        fields=[
            'exclude_from_collection',
        ],
    )
    directives.widget(exclude_from_collection=SingleCheckBoxBoolFieldWidget)
    exclude_from_collection = schema.Bool(
        title=_(
            "Exclude from Collection",
        ),
        description=_(
            'If this is enabled, one can filter out this object in a collection by using "Exclude from Collection: False"',
        ),
        required=False,
        default=False,
    )


@implementer(IExcludeFromCollection)
@adapter(IExcludeFromCollectionMarker)
class ExcludeFromCollection(object):
    def __init__(self, context):
        self.context = context

    @property
    def exclude_from_collection(self):
        if safe_hasattr(self.context, "exclude_from_collection"):
            return self.context.exclude_from_collection
        return None

    @exclude_from_collection.setter
    def exclude_from_collection(self, value):
        self.context.exclude_from_collection = value
