# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

from collective.excludefromcollection.behaviors.exclude_from_collection import (
    IExcludeFromCollectionMarker,
)
from collective.excludefromcollection.testing import (  # noqa
    COLLECTIVE_EXCLUDEFROMCOLLECTION_INTEGRATION_TESTING,
)


class ExcludeFromCollectionIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_EXCLUDEFROMCOLLECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_exclude_from_collection(self):
        behavior = getUtility(
            IBehavior, "collective.excludefromcollection.exclude_from_collection"
        )
        self.assertEqual(
            behavior.marker,
            IExcludeFromCollectionMarker,
        )
