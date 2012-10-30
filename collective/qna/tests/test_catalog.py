from plone.app.testing import login

from .base import IntegrationTestCase
from .base import MANAGER_ID


class ForumBrowserViewTest(IntegrationTestCase):

    def setUp(self):
        portal = self.layer['portal']
        login(portal, MANAGER_ID)

        # Create a forum to put questions in
        portal.invokeFactory(type_name="qna_forum", id="qna")

    def test_catalog_installed(self):
        indexes = self.layer['portal'].portal_catalog.indexes()
        self.assertTrue('qna_total_answers' in indexes)

    def test_total_answers(self):
        """Should equal the number of answer nodes
        """
        forum = self.layer['portal']['qna']

        forum.invokeFactory(type_name="qna_question", id="question1")
        qn = forum['question1']
        for i in range(0, 5):
            qnItem = forum.restrictedTraverse('@@folderListing')(
                id="question1",
            )[0]
            self.assertEquals(qnItem.qna_total_answers, i)

            qn.invokeFactory(type_name="qna_answer", id="answer%d" % i)
            qn.reindexObject()
