# -*- coding: utf-8 -*-

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from collective.excludefromcollection.behaviors.exclude_from_collection import (
    IExcludeFromCollectionMarker,
)


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IExcludeFromCollectionMarker)
def exclude_from_collection(obj):
    """Calculate and return the value for the indexer"""
    return obj.exclude_from_collection
