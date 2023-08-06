# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2

import collective.excludefromcollection


class CollectiveExcludefromcollectionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.excludefromcollection)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.excludefromcollection:default")


COLLECTIVE_EXCLUDEFROMCOLLECTION_FIXTURE = CollectiveExcludefromcollectionLayer()


COLLECTIVE_EXCLUDEFROMCOLLECTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EXCLUDEFROMCOLLECTION_FIXTURE,),
    name="CollectiveExcludefromcollectionLayer:IntegrationTesting",
)


COLLECTIVE_EXCLUDEFROMCOLLECTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EXCLUDEFROMCOLLECTION_FIXTURE,),
    name="CollectiveExcludefromcollectionLayer:FunctionalTesting",
)


COLLECTIVE_EXCLUDEFROMCOLLECTION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EXCLUDEFROMCOLLECTION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveExcludefromcollectionLayer:AcceptanceTesting",
)
