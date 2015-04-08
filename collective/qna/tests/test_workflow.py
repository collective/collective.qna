from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.WorkflowCore import WorkflowException

from plone.app.testing import login

from .base import IntegrationTestCase
from .base import MANAGER_ID, USER_A_ID, USER_B_ID


class WorkflowTest(IntegrationTestCase):

    def setUp(self):
        portal = self.layer['portal']

        # Create forum with on question and answer
        login(portal, MANAGER_ID)
        portal.invokeFactory(type_name="qna_forum", id="qna")
        login(portal, USER_A_ID)
        portal['qna'].invokeFactory(type_name="qna_question", id="question-a")
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer",
                                                  id="answer-a")

    def test_contentinitiallypublished(self):
        """Question and answers should be published by default
        """
        portal = self.layer['portal']
        workflow = portal.portal_workflow

        # All are published
        self.assertEqual(
            workflow.getInfoFor(portal['qna'], 'review_state'),
            'published',
        )
        self.assertEqual(
            workflow.getInfoFor(portal['qna']['question-a'], 'review_state'),
            'published',
        )
        self.assertEqual(
            workflow.getInfoFor(portal['qna']['question-a']['answer-a'],
                                'review_state'),
            'published',
        )

        # Only the manager can edit the forum
        self.assertEquals(
            self._havePermission(
                portal['qna'],
                ModifyPortalContent
            ),
            [MANAGER_ID],
        )

        # Everyone can view question
        self.assertEquals(
            self._havePermission(portal['qna']['question-a'], View),
            [MANAGER_ID, USER_A_ID, USER_B_ID],
        )

        # The manager and owner can edit question
        self.assertEquals(
            self._havePermission(
                portal['qna']['question-a'],
                ModifyPortalContent
            ),
            [MANAGER_ID, USER_A_ID],
        )

        # Everyone can view answer
        self.assertEquals(
            self._havePermission(
                portal['qna']['question-a']['answer-a'],
                View,
            ),
            [MANAGER_ID, USER_A_ID, USER_B_ID],
        )

        # The manager and owner can edit answer
        self.assertEquals(
            self._havePermission(
                portal['qna']['question-a']['answer-a'],
                ModifyPortalContent
            ),
            [MANAGER_ID, USER_A_ID],
        )

    def test_questionmoderation(self):
        """Question and answers can be hidden from view
        """
        portal = self.layer['portal']
        item = portal['qna']['question-a']

        # Only a manager can hide content
        login(portal, USER_A_ID)
        with self.assertRaisesRegexp(WorkflowException,
                                     'No workflow provides'):
            self._callTransition(item, 'hide', 'hidden')
        login(portal, MANAGER_ID)
        self._callTransition(item, 'hide', 'hidden')

        # The manager only can view question
        self.assertEquals(
            self._havePermission(portal['qna']['question-a'], View),
            [MANAGER_ID],
        )

        # The manager only can edit question
        self.assertEquals(
            self._havePermission(
                portal['qna']['question-a'],
                ModifyPortalContent
            ),
            [MANAGER_ID],
        )

        # Only a manager can publish content
        login(portal, USER_A_ID)
        with self.assertRaisesRegexp(WorkflowException,
                                     'No workflow provides'):
            self._callTransition(item, 'publish', 'published')
        login(portal, MANAGER_ID)
        self._callTransition(item, 'publish', 'published')

        # Everyone can view question again
        self.assertEquals(
            self._havePermission(portal['qna']['question-a'], View),
            [MANAGER_ID, USER_A_ID, USER_B_ID],
        )

    def _havePermission(self, obj, permission):
        out = []
        for userId in [MANAGER_ID, USER_A_ID, USER_B_ID]:
            login(self.layer['portal'], userId)
            if getSecurityManager().checkPermission(permission, obj):
                out.append(userId)
        return out

    def _callTransition(self, ob, transition, new_state):
        """Transition content into different wf state
        """
        portal = self.layer['portal']
        workflow = portal.portal_workflow
        workflow.doActionFor(ob, transition)
        self.assertEquals(
            workflow.getInfoFor(ob, 'review_state'),
            new_state,
        )
