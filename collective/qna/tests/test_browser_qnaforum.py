from datetime import datetime, timedelta

from Products.ATContentTypes.utils import dt2DT

from plone.app.testing import login

from .base import IntegrationTestCase
from .base import MANAGER_ID


class ForumBrowserViewTest(IntegrationTestCase):

    def test_mostrecent(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        login(portal, MANAGER_ID)

        # Create a bunch of questions with different times
        portal.invokeFactory(type_name="qna_forum", id="qna")
        forum = portal['qna']
        for i in range(1, 26):
            id = "question" + str(i)
            forum.invokeFactory(
                type_name="qna_question",
                id=id,
                title="Question " + str(i),
            )
            forum[id].creation_date = dt2DT(datetime.now()
                                            - timedelta(hours=30 - i))
            forum[id].reindexObject()

        # Should get first 10 results
        listing = forum.restrictedTraverse('@@most-recent').questionListing()
        self.assertEquals(len(listing), 10)
        for i, qn in enumerate(range(25, 16, -1)):
            self.assertEquals(listing[i].id, 'question' + str(qn))

        # Get next 10 results
        self.layer['request'].set('page', 2)
        listing = forum.restrictedTraverse('@@most-recent').questionListing()
        self.assertEquals(len(listing), 10)
        for i, qn in enumerate(range(15, 6, -1)):
            self.assertEquals(listing[i].id, 'question' + str(qn))
