from  jornada.contenttypes.testing import JORNADA_CONTENTTYPES_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_test.txt"),
                layer=JORNADA_CONTENTTYPES_FUNCTIONAL_TESTING)
    ])
    return suite