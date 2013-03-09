# -*- coding: utf-8 -*-

from five import grok
from jornada.contenttypes.controlpanel import IJornadaSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import unicodedata


def _normalize_token(token):
    """Normalize a token using ascii as encoding.
    """
    normalize = unicodedata.normalize
    return normalize('NFKD', token).encode('ascii', 'ignore').lower()


class SectionsVocabulary(object):
    """Creates a vocabulary with the available sections stored in the
    registry; the vocabulary is normalized to allow the use of non-ASCII
    characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IJornadaSettings)
        available_sections = list(settings.available_sections)
        available_sections.sort()
        items = []
        for section in available_sections:
            token = _normalize_token(section)
            items.append(SimpleVocabulary.createTerm(section, token, section))
        return SimpleVocabulary(items)

grok.global_utility(SectionsVocabulary,
                    name=u'jornada.contenttypes.AvailableSections')
