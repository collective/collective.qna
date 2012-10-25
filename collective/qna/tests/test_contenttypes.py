from plone.app.testing import setRoles, TEST_USER_ID

from .base import IntegrationTestCase


class ContentTypeTest(IntegrationTestCase):

    def test_createcontent(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory(type_name="qna_forum", id="qna")
        portal['qna'].invokeFactory(type_name="qna_question", id="question")
        portal['qna']['question'].invokeFactory(type_name="qna_answer", id="answer")
        with self.assertRaisesRegexp(ValueError, 'qna_question'):
            portal.invokeFactory(type_name="qna_question", id="qna")
        with self.assertRaisesRegexp(ValueError, 'qna_answer'):
            portal.invokeFactory(type_name="qna_answer", id="qna")
