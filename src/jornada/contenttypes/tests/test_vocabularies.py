# -*- coding: utf-8 -*-

from jornada.contenttypes.controlpanel import IJornadaSettings
from jornada.contenttypes.testing import JORNADA_CONTENTTYPES_INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IJornadaSettings)

    def test_available_sections_vocabulary(self):
        name = 'jornada.contenttypes.AvailableSections'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)
        sections = util(self.portal)
        # FIXME: we need to set up at least one section
        self.assertEqual(len(sections), 0)
        #self.assertTrue(u'Default' in sections)

    def test_available_sections_vocabulary_is_sorted(self):
        self.settings.available_sections = set([u"5", u"4", u"3", u"2", u"1"])
        name = 'jornada.contenttypes.AvailableSections'
        util = queryUtility(IVocabularyFactory, name)
        sections = util(self.portal)
        sections = [i.title for i in sections]
        self.assertListEqual(sections, [u"1", u"2", u"3", u"4", u"5"])
