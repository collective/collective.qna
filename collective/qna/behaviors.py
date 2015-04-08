import re

from zope import schema
from zope.interface import implements, alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from z3c.form.interfaces import IDisplayForm
from z3c.form.object import registerFactoryAdapter

from plone.autoform import directives, interfaces
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel import model
from plone.dexterity.content import Container

from collective.qna import _


class AnswersVocab(object):
    implements(IVocabularyFactory)
    """Make a vocabulary of current answer
    """

    def __new__(self, context):
        """Turn a content listing into a vocabulary"""
        def shorten(s):
            if len(s) > 20:
                s = s[0:20] + '...'
            s = re.compile('\s+').sub(' ', s)
            return s

        listing = context.restrictedTraverse('@@folderListing')()
        return SimpleVocabulary([
            SimpleVocabulary.createTerm(item.id,
                                        item.id,
                                        shorten(item.answer))
            for item in listing
        ])


class IForum(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IForum, interfaces.IFormFieldProvider)


class IQuestion(model.Schema):
    """A question in the QnA forum
    """

    directives.omitted('best_answer')
    directives.no_omit(IDisplayForm, 'best_answer')
    best_answer = schema.Choice(
        title=_(u'Best answer'),
        vocabulary='collective.qna.answers',
        required=False)
alsoProvides(IQuestion, interfaces.IFormFieldProvider)


class IAnswer(model.Schema):
    """An answer to a question
    """

    directives.omitted('score')
    directives.no_omit(IDisplayForm, 'score')
    score = schema.Int(
        title=_(u'Answer score'),
        required=False)
alsoProvides(IAnswer, interfaces.IFormFieldProvider)
