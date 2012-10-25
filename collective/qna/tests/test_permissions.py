from AccessControl.unauthorized import Unauthorized
from Products.CMFCore.utils import getToolByName

from plone.app.testing import setRoles, login

from .base import IntegrationTestCase
from .base import MANAGER_ID, USER_A_ID, USER_B_ID, USER_C_ID


class PermissionsTest(IntegrationTestCase):

    def test_createcontent(self):
        """Ensure permissions hold for various roles
        """
        portal = self.layer['portal']
        login(portal, MANAGER_ID)
        portal.invokeFactory(type_name="qna_forum", id="qna")

        # User A can't create a forum, but they can add a question and answer
        login(portal, USER_A_ID)
        with self.assertRaisesRegexp(Unauthorized, 'qna_forum'):
            portal.invokeFactory(type_name="qna_forum", id="qna1")
        portal['qna'].invokeFactory(type_name="qna_question", id="question")
        portal['qna']['question'].invokeFactory(type_name="qna_answer"
                                               , id="answer1")

        # ...so can User B
        login(portal, USER_B_ID)
        portal['qna']['question'].invokeFactory(type_name="qna_answer"
                                               , id="answer2")
