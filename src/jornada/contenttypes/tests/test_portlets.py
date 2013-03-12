# -*- coding: utf-8 -*-

from jornada.contenttypes.portlets import articles
from jornada.contenttypes.testing import JORNADA_CONTENTTYPES_INTEGRATION_TESTING
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class TestArticlesPortlet(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.Articles')
        self.assertEqual(portlet.addview, 'portlets.Articles')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.Articles')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual([
            'plone.app.portlets.interfaces.IColumn',
            'plone.app.portlets.interfaces.IDashboard',
            ], registered_interfaces)

    def testInterfaces(self):
        portlet = articles.Assignment(count=5)
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))
