from Products.Five import BrowserView
from zope.security import checkPermission


class QuestionView(BrowserView):
    def canEditContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def markBestAnswer(self):
        bestId = self.request.get('id', '')
        if len(self.context
                   .restrictedTraverse('@@folderListing')(id=bestId)) != 1:
            raise ValueError(bestId)
        self.context.best_answer = bestId
        self.request.response.redirect(self.context.absolute_url())
