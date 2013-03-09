# -*- coding:utf-8 -*-

from five import grok
from jornada.contenttypes import _
from plone.app.textfield import RichText
from plone.dexterity import content
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

grok.templatedir('templates')


class IArticle(form.Schema):
    """An article. Defines a news article.
    """

    subtitle = schema.TextLine(
        title=_(u"Subtitle"),
    )

    author = schema.TextLine(
        title=_(u"Author"),
    )

    text = RichText(
        title=_(u"Text"),
    )

    section = schema.Choice(
        title=_(u"Section"),
        vocabulary='jornada.contenttypes.AvailableSections',
    )

    location = schema.TextLine(
        title=_(u"Location"),
    )

    image = NamedBlobImage(
        title=_(u"Image")
    )


class Article(content.Item):
    """My class"""


class View(grok.View):
    grok.context(IArticle)
    grok.require('zope2.View')
    grok.name('my-view')
