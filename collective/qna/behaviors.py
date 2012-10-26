from zope.interface import implements, alsoProvides

from zope import schema
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.form.interfaces import IDisplayForm
from z3c.form.object import registerFactoryAdapter

from plone.autoform import directives, interfaces
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel import model
from plone.dexterity.content import Container

from collective.qna import _


class IForum(model.Schema):
    """The top of a QnA form
    """
alsoProvides(IForum, interfaces.IFormFieldProvider)


class IQuestion(model.Schema):
    """A question in the QnA forum
    """

    #TODO: Vocab for answers
    directives.omitted('best_answer')
    directives.no_omit(IDisplayForm, 'best_answer')
    best_answer = schema.TextLine(
        title=_(u'Best answer'),
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
