from zope.interface import implements

from zope import schema
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.form.interfaces import IDisplayForm
from z3c.form.object import registerFactoryAdapter

from plone.autoform import directives
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel import model
from plone.dexterity.content import Container

from collective.qna import _

class IForum(model.Schema):
    """The top-level content type that contains questions
    """

class IQuestion(model.Schema):
    """A question in the QnA forum
    """

    content = RichText(
        title=_(u'Ask your question'),
        required=False)

    #TODO: Vocab for answers
    directives.omitted('best_answer')
    directives.no_omit(IDisplayForm, 'best_answer')
    best_answer = schema.TextLine(
        title=_(u'Best answer'),
        required=False)

class IAnswer(model.Schema):
    """An answer to a question
    """

    content = RichText(
        title=_(u'Your answer'),
        required=False)

    directives.omitted('score')
    directives.no_omit(IDisplayForm, 'score')
    score = schema.Int(
        title=_(u'Answer score'),
        required=False)
