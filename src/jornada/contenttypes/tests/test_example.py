import unittest

from Products.CMFCore.utils import getToolByName

from jornada.contenttypes.testing import \
    JORNADA_CONTENTTYPES_INTEGRATION_TESTING


class InstallTestCase(unittest.TestCase):

    layer = JORNADA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        pid = 'jornada.contenttypes'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertIn(pid, installed,
                      'package appears not to have been installed')

    def test_dependencies_are_installed(self):
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertIn('plone.app.dexterity', installed,
                      'plone.app.dexterity not installed')

    def test_add_permission(self):
        permission = 'jornada.contenttypes: Add Article'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)
