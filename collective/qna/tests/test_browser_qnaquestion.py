from AccessControl.unauthorized import Unauthorized

from plone.app.testing import login

from .base import IntegrationTestCase
from .base import MANAGER_ID, USER_A_ID, USER_B_ID


class QuestionBrowserViewTest(IntegrationTestCase):
    def setUp(self):
        """Make the qna forum
        """
        portal = self.layer['portal']
        login(portal, MANAGER_ID)
        portal.invokeFactory(type_name="qna_forum", id="qna")

        # A asks a question and answers it
        login(portal, USER_A_ID)
        portal['qna'].invokeFactory(type_name="qna_question", id="question-a")
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer",
                                                  id="answer-a")

        # B gives 2 answers
        login(portal, USER_B_ID)
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer",
                                                  id="answer-b1")
        portal['qna']['question-a'].invokeFactory(type_name="qna_answer",
                                                  id="answer-b2")

    def test_caneditcontent(self):
        """Test only owners can edit content
        """
        portal = self.layer['portal']
        qn = portal['qna']['question-a']

        from zope.security.management import newInteraction
        newInteraction()

        # User A can edit the question
        login(portal, USER_A_ID)
        self.assertTrue(qn.restrictedTraverse('@@view').canEditContent())

        # User B can't edit the question
        login(portal, USER_B_ID)
        self.assertFalse(qn.restrictedTraverse('@@view').canEditContent())

    def test_markbestanswer(self):
        """Test only owners can choose best answer
        """
        portal = self.layer['portal']
        request = self.layer['request']
        qn = portal['qna']['question-a']

        # User B isn't allowed to mark a best answer
        login(portal, USER_B_ID)
        with self.assertRaisesRegexp(Unauthorized, 'mark-best-answer'):
            qn.restrictedTraverse('@@mark-best-answer')()

        # User A has to supply an id
        login(portal, USER_A_ID)
        with self.assertRaises(ValueError):
            qn.restrictedTraverse('@@mark-best-answer')()

        # User A has to supply a valid id
        login(portal, USER_A_ID)
        request['id'] = 'flannelflannelflannel'
        with self.assertRaisesRegexp(ValueError, 'flannelflannelflannel'):
            qn.restrictedTraverse('@@mark-best-answer')()

        # User A can set a valid id
        login(portal, USER_A_ID)
        request['id'] = 'answer-b1'
        qn.restrictedTraverse('@@mark-best-answer')()
        self.assertEquals(qn.best_answer, 'answer-b1')
        request['id'] = 'answer-a'
        qn.restrictedTraverse('@@mark-best-answer')()
        self.assertEquals(qn.best_answer, 'answer-a')
