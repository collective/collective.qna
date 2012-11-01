from Products.Five import BrowserView


class ForumView(BrowserView):
    """Base class for all IForum-ish things
    """
    batch_size = 10

    def __init__(self, context, request):
        super(ForumView, self).__init__(context, request)
        page = request.get('page', 1)
        self.batch_start = (page - 1) * self.batch_size
        self.query = dict(
            batch=True,
            b_start=self.batch_start,
            b_size=self.batch_size,
            sort_on='created',
            sort_order='descending',
        )


class MostRecent(ForumView):
    """All questions, most recent first
    """

    def questionListing(self):
        listing = self.context.restrictedTraverse('@@folderListing')(**dict(
            self.query
        ))
        return [item for item in listing if item.isVisibleInNav()]


class MostActivity(ForumView):
    """All questions, 
    """

    pass


class AllUnanswered(ForumView):
    """All questions currently without answers
    """

    def questionListing(self):
        listing = self.context.restrictedTraverse('@@folderListing')(**dict(
            self.query,
            qna_total_answers=0,
        ))
        return [item for item in listing if item.isVisibleInNav()]


class ByCategory(ForumView):
    """All questions marked with a category
    """

    def questionListing(self):
        category = self.request.get('category', None)
        listing = self.context.restrictedTraverse('@@folderListing')(**dict(
            self.query,
            Subject=category,
        ))
        return [item for item in listing if item.isVisibleInNav()]
