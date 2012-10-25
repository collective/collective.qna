from Products.CMFCore.utils import getToolByName

from plone.app.testing import setRoles, TEST_USER_ID

from .base import IntegrationTestCase


class ContentTypeTest(IntegrationTestCase):

    def test_createcontent(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
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
