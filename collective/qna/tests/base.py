from unittest import TestCase

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from zope.configuration import xmlconfig

from Products.CMFCore.utils import getToolByName


class QnAFixture(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)
    USER_A_ID = "Arnold"
    USER_B_ID = "Betty"
    USER_C_ID = "Caroline"
    MANAGER_ID = "BigBoss"

    def setUpZope(self, app, configurationContext):
        import collective.qna
        xmlconfig.include(configurationContext, 'configure.zcml', collective.qna)
        configurationContext.execute_actions()

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.qna:default')

        # Creates some users
        acl_users = getToolByName(portal, 'acl_users')
        for id in [self.USER_A_ID, self.USER_B_ID, self.USER_C_ID]:
            acl_users.userFolderAddUser(
                id, 'secret'+id[0],
                ['Member'],[]
            )
        acl_users.userFolderAddUser(
            self.MANAGER_ID, 'secretBB',
            ['Manager'],[]
        )

    def tearDownPloneSite(self, portal):
        pass


FIXTURE = QnAFixture()

COLLECTIVE_QNA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="collective.qna:Integration",
    )
COLLECTIVE_QNA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="collective.qna:Functional",
    )


class IntegrationTestCase(TestCase):
    layer = COLLECTIVE_QNA_INTEGRATION_TESTING


class FunctionalTestCase(TestCase):
    layer = COLLECTIVE_QNA_FUNCTIONAL_TESTING
