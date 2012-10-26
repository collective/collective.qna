from datetime import datetime, timedelta

from Products.ATContentTypes.utils import dt2DT
from Products.CMFCore.utils import getToolByName

from plone.app.testing import setRoles, login

from .base import IntegrationTestCase
from .base import MANAGER_ID, USER_A_ID, USER_B_ID, USER_C_ID


class ForumBrowserViewTest(IntegrationTestCase):

    def test_mostrecent(self):
        """Content types can be created and nested appropriately
        """
        portal = self.layer['portal']
        login(portal, MANAGER_ID)
        wftool = getToolByName(portal, 'portal_workflow')

        portal.invokeFactory(type_name="qna_forum", id="qna")
        forum = portal['qna']
        forum.invokeFactory(type_name="qna_question", id="question1", title="Question 1")
        forum['question1'].creation_date = dt2DT(datetime.now() - timedelta(hours=5))
        forum['question1'].reindexObject()
        forum.invokeFactory(type_name="qna_question", id="question2", title="Question 2")
        forum['question2'].creation_date = dt2DT(datetime.now() - timedelta(hours=4))
        forum['question2'].reindexObject()
        forum.invokeFactory(type_name="qna_question", id="question3", title="Question 3")
        forum['question3'].creation_date = dt2DT(datetime.now() - timedelta(hours=3))
        forum['question3'].reindexObject()
        forum.invokeFactory(type_name="qna_question", id="question4", title="Question 4")
        forum['question4'].creation_date = dt2DT(datetime.now() - timedelta(hours=2))
        forum['question4'].reindexObject()
        forum.invokeFactory(type_name="qna_question", id="question5", title="Question 5")
        forum['question5'].creation_date = dt2DT(datetime.now() - timedelta(hours=1))
        forum['question5'].reindexObject()
        listing = forum.restrictedTraverse('@@most-recent').questionListing()
        self.assertEquals(listing[0].id, 'question5')
        self.assertEquals(listing[1].id, 'question4')
        self.assertEquals(listing[2].id, 'question3')
        self.assertEquals(listing[3].id, 'question2')
        self.assertEquals(listing[4].id, 'question1')
