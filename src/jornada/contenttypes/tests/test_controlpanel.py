# -*- coding: utf-8 -*-

from jornada.contenttypes.controlpanel import IJornadaSettings
from jornada.contenttypes.testing import JORNADA_CONTENTTYPES_INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='jornada-settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@jornada-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('jornada', actions, 'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['jornada.contenttypes'])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('jornada', actions, 'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IJornadaSettings)

    def test_available_sections_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'available_sections'))
        self.assertEqual(self.settings.available_sections, set())

    def test_default_section_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_section'))
        self.assertEqual(self.settings.default_section, None)

    def test_records_removed_on_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['jornada.contenttypes'])

        BASE_REGISTRY = 'jornada.contenttypes.controlpanel.IJornadaSettings.%s'
        records = (
            BASE_REGISTRY % 'available_sections',
            BASE_REGISTRY % 'default_section',
        )

        for r in records:
            self.assertNotIn(r, self.registry)
