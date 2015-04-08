from AccessControl import getSecurityManager
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
        portal['qna'].invokeFactory(type_name="qna_question", id="question-a")
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer"
                                               , id="answer-a")

        # ...so can User B
        login(portal, USER_B_ID)
        with self.assertRaisesRegexp(Unauthorized, 'qna_forum'):
            portal.invokeFactory(type_name="qna_forum", id="qna1")
        portal['qna'].invokeFactory(type_name="qna_question", id="question-b")
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer"
                                               , id="answer-b")
        portal['qna']['question-b'].invokeFactory(type_name="qna_answer"
                                               , id="answer-b")

        # User A owns it's own questions and answers, but not B's
        login(portal, USER_A_ID)
        user = getSecurityManager().getUser()
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']),
            ['Owner', 'Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']['answer-a']),
            ['Owner', 'Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']['answer-b']),
            ['Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-b']),
            ['Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-b']['answer-b']),
            ['Member', 'Authenticated'])

        # User B owns it's own questions and answers, but not A's
        login(portal, USER_B_ID)
        user = getSecurityManager().getUser()
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']),
            ['Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']['answer-a']),
            ['Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-a']['answer-b']),
            ['Owner', 'Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-b']),
            ['Owner', 'Member', 'Authenticated'])
        self.assertEquals(
            user.getRolesInContext(portal['qna']['question-b']['answer-b']),
            ['Owner', 'Member', 'Authenticated'])
