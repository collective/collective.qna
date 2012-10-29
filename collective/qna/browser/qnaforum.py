from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ForumView(BrowserView):
    """Base class for all IForum-ish things
    """
    question_template = ViewPageTemplateFile('qna_question_fragment.pt')
    batch_size = 10

    def __init__(self, context, request):
        super(ForumView, self).__init__(context, request)
        page = request.get('page', 1)
        self.batch_start = (page - 1) * self.batch_size

    def renderQuestion(self, question):
        return self.question_template(
            question=question,
        )


class MostRecent(ForumView):
    """All questions, most recent first
    """

    def questionListing(self):
        listing = self.context.restrictedTraverse('@@folderListing')(
            batch=True,
            b_start=self.batch_start,
            b_size=self.batch_size,
            sort_on='created',
            sort_order='descending',
        )
        return [item for item in listing if item.isVisibleInNav()]


class MostActivity(ForumView):
    """All questions, 
    """

    pass


class AllUnanswered(ForumView):
    """All questions currently without answers
    """

    pass
