from Products.CMFCore.utils import getToolByName

from plone.app.testing import setRoles, login

from .base import IntegrationTestCase
from .base import MANAGER_ID, USER_A_ID, USER_B_ID, USER_C_ID


class ContentTypeTest(IntegrationTestCase):

    def test_createcontent(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        login(portal, MANAGER_ID)
        wftool = getToolByName(portal, 'portal_workflow')

        portal.invokeFactory(type_name="qna_forum", id="qna")
        item = portal['qna']
        self.assertEquals(wftool.getInfoFor(item, 'review_state'), 'published')

        item.invokeFactory(type_name="qna_question", id="question")
        item = portal['qna']['question']
        self.assertEquals(wftool.getInfoFor(item, 'review_state'), 'published')

        item.invokeFactory(type_name="qna_answer", id="answer")
        item = portal['qna']['question']['answer']
        self.assertEquals(wftool.getInfoFor(item, 'review_state'), 'published')

        # Create content in the wrong places
        with self.assertRaisesRegexp(ValueError, 'qna_question'):
            portal.invokeFactory(type_name="qna_question", id="qna")
        with self.assertRaisesRegexp(ValueError, 'qna_answer'):
            portal.invokeFactory(type_name="qna_answer", id="qna")
