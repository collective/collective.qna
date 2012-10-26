from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ForumView(BrowserView):
    """Base class for all IForum-ish things
    """
    question_template = ViewPageTemplateFile('qna_question_fragment.pt')

    def renderQuestion(self, question):
        return self.question_template(
            question=question,
        )


class MostRecent(ForumView):
    """All questions, most recent first
    """

    def questionListing(self):
        listing = self.context.restrictedTraverse('@@folderListing')(
            sort_on='created',
            sort_order='descending',
        )
        #TODO: Pagination
        return [item for item in listing if item.isVisibleInNav()]


class MostActivity(ForumView):
    """All questions, 
    """

    pass


class AllUnanswered(ForumView):
    """All questions currently without answers
    """

    pass
