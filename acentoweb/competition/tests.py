import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import acentoweb.competition


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(acentoweb.competition)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

ptc.setupPloneSite(products=['acentoweb.competition'])

class TestWorkflow(TestCase):
    def test_wf_exists(self):
        wt = self.portal.portal_workflow
        self.failUnless('competition_workflow' in wt.objectIds())


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='acentoweb.competition',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='acentoweb.competition.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

            unittest.makeSuite(TestWorkflow)

        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='acentoweb.competition',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='acentoweb.competition',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
