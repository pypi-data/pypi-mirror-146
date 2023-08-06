# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from collective.excludefromcollection.testing import (
    COLLECTIVE_EXCLUDEFROMCOLLECTION_FUNCTIONAL_TESTING,
    COLLECTIVE_EXCLUDEFROMCOLLECTION_INTEGRATION_TESTING,
)


class IndexerIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_EXCLUDEFROMCOLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_dummy(self):
        self.assertTrue(True)


class IndexerFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_EXCLUDEFROMCOLLECTION_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_dummy(self):
        self.assertTrue(True)
