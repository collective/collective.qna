from datetime import datetime, timedelta

from Products.ATContentTypes.utils import dt2DT

from plone.app.testing import login

from .base import IntegrationTestCase
from .base import MANAGER_ID


class ForumBrowserViewTest(IntegrationTestCase):

    def setUp(self):
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
                # Tag content with what it's divisible by
                subject=(["divisible by %d" % j for j in range(2, 10)
                                                if i % j == 0])
            )
            forum[id].creation_date = dt2DT(datetime.now()
                                            - timedelta(hours=30 - i))
            forum[id].reindexObject()

    def test_mostrecent(self):
        """Content types can be created and nested appropriately
        """
        forum = self.layer['portal']['qna']

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

    def test_bycategory(self):
        """Content types can be created and nested appropriately
        """
        forum = self.layer['portal']['qna']

        # Should get first 10 results
        self.layer['request'].set('category', 'divisible by 2')
        listing = forum.restrictedTraverse('@@by-category').questionListing()
        self.assertEquals(len(listing), 10)
        self.assertEquals(listing[0].id, 'question24')
        self.assertEquals(listing[1].id, 'question22')
        self.assertEquals(listing[2].id, 'question20')
        self.assertEquals(listing[3].id, 'question18')
        self.assertEquals(listing[4].id, 'question16')
        self.assertEquals(listing[5].id, 'question14')
        self.assertEquals(listing[6].id, 'question12')
        self.assertEquals(listing[7].id, 'question10')
        self.assertEquals(listing[8].id, 'question8')
        self.assertEquals(listing[9].id, 'question6')

        self.layer['request'].set('category', 'divisible by 3')
        listing = forum.restrictedTraverse('@@by-category').questionListing()
        self.assertEquals(len(listing), 8)
        self.assertEquals(listing[0].id, 'question24')
        self.assertEquals(listing[1].id, 'question21')
        self.assertEquals(listing[2].id, 'question18')
        self.assertEquals(listing[3].id, 'question15')
        self.assertEquals(listing[4].id, 'question12')
        self.assertEquals(listing[5].id, 'question9')
        self.assertEquals(listing[6].id, 'question6')
        self.assertEquals(listing[7].id, 'question3')
