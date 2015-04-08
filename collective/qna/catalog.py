from plone.indexer import indexer

from .behaviors import IQuestion


@indexer(IQuestion)
def qna_total_answers(object):
    """Total number of answers withn question
    """
    listing = object.restrictedTraverse('@@folderListing')()
    return listing.actual_result_count
