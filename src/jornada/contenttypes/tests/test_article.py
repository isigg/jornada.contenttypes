# -*- coding: utf-8 -*-

from jornada.contenttypes.article import IArticle
from jornada.contenttypes.testing import JORNADA_CONTENTTYPES_INTEGRATION_TESTING
from plone.app.customerize import registration
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import directlyProvides
from zope.interface import Interface
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.uuid.interfaces import IAttributeUUID

import unittest


class ArticleTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Article', 'a1')
        self.a1 = self.folder['a1']

    def test_adding(self):
        self.assertTrue(IArticle.providedBy(self.a1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        schema = fti.lookupSchema()
        self.assertEqual(schema, IArticle)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IArticle.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.a1))
        self.assertTrue(IAttributeUUID.providedBy(self.a1))


class ArticleViewIntegrationTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        #directlyProvides(self.request, ILayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Article', 'a1')
        self.a1 = self.folder['a1']

    def test_default_view_is_registered(self):
        pt = self.portal['portal_types']
        self.assertEqual(pt['Article'].default_view, 'view')

        registered = [v.name for v in registration.getViews(Interface)]
        self.assertIn('view', registered)
